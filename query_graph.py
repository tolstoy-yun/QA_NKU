# coding: utf-8
from py2neo import Graph, Node, Relationship,NodeMatcher
from zhon.hanzi import punctuation
import re
from triple_extraction import*

class Query_Graph:
    graph=None
    extra=TripleExtractor()

    def __init__(self):
        #与neo4j建立连接
        self.graph = Graph(
            "http://localhost:7474",
            username="neo4j",
            password="590764"
        )
    #查询
    def query(self,sentence):
        query_word=["哪","什么","呢","吗","谁","怎么样","怎么","如何","多久","多少"]
        query_sentence = re.sub(r"[{}]+".format(punctuation), "", sentence)  # 将标点符号转化为空格
        #print(query_sentence)
        svos=self.extra.triples_main(query_sentence)
        #print(svos)
        query_type=0 #问句类型，1为主谓问宾语，2为谓宾问主语，0为其他无法回答的问题
        if(svos==[]):
            query_type=0
        else:
            for word in query_word:
                if word in svos[0][2]:
                    query_type=1
                    break
                if word in svos[0][0]:
                    query_type=2
                    break
        #print(query_type)
        #有主谓问宾语
        if query_type==1:
            p_name=".*"+svos[0][0]+".*"
            r_name=".*"+svos[0][1]+".*"
            data = self.graph.run(
                "match(p) -[r]->(n) where p.Name=~'%s' AND r.relation=~'%s' return n.Name LIMIT 1" % (p_name,r_name)
            )
            result=""
            for a in data:
                for item in a.items():
                    result=item[1]
            if result!="":
                print("答："+result)
            else:
                print("答：我的智商有限，暂时回答不了您的问题呢~")
        #有谓宾问主语
        elif query_type==2:
            n_name=".*"+svos[0][2]+".*"
            r_name=".*"+svos[0][1]+".*"
            data = self.graph.run(
                "match(p) -[r]->(n) where n.Name=~'%s' AND r.relation=~'%s' return p.Name LIMIT 1" % (n_name,r_name)
            )
            result=""
            for a in data:
                for item in a.items():
                    result=item[1]
            if result!="":
                print("答："+result)
            else:
                print("答：我的智商有限，暂时回答不了您的问题呢~")
        else:
            print("答：我的智商有限，暂时回答不了您的问题呢~")

if __name__=='__main__':
    query_graph=Query_Graph()
    print("输入“close”即可关闭程序")
    """
    测试样例：
        南开大学成立于哪年？
        叶嘉莹毕业于哪里？
        现任校长是谁？
        谁考察了南开大学？
        汉语言文化学院成立于哪年？
    """
    while(1):
        sentence=input("问：")
        if sentence=="close":
            print("江湖再会！")
            break
        query_graph.query(sentence)
    