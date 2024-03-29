from py2neo import Graph, Node, Relationship,NodeMatcher

class Create_Graph:
    graph=None
    triple_dir="./triple/" # 存放三元组的路径

    def __init__(self):
        #与neo4j建立连接
        self.graph = Graph(
            "http://localhost:7474",
            username="neo4j",
            password="590764"
        )

    #建知识图谱
    def create(self):
        with open(self.triple_dir+"triple.txt",encoding="utf_8")as f:
            #对每一个三元组，建立联系
            for line in f.readlines():
                rela_array=line.strip("\n").split(",")
                print(rela_array)
                """
                将每一个三元组x,y,z放入neo4j图数据库中，x为subject节点，y为关系relation，z为object节点
                x指向y，两者的关系为z
                """
                try:
                    self.graph.run("MERGE(p: Subject{Name: '%s'})"%(rela_array[0]))
                    self.graph.run("MERGE(p: Object{Name: '%s'})" % (rela_array[2]))
                    self.graph.run(
                        "MATCH(e: Subject), (cc: Object) \
                        WHERE e.Name='%s' AND cc.Name='%s'\
                        CREATE(e)-[r:Predicate{relation: '%s'}]->(cc)\
                        RETURN r" % (rela_array[0], rela_array[2], rela_array[1])
                    )
                except Exception:
                    continue

creategraph = Create_Graph()
creategraph.create()
