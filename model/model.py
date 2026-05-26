import networkx as nx

from database.DAO import DAO


class Model:

    def __init__(self):
        self._graph = nx.Graph()
        self._nodes = []
        self.idMap={}

    def creategraph(self, anno:int):
        self._graph.clear()
        self.addnodes(anno)
        self.addedges(anno)
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def addnodes(self, anno:int):
        for c in DAO.getallcountries(anno):
            self._nodes.append(c)
            self._graph.add_node(c)
            self.idMap[c.CCode] = c

    def addedges(self, year:int):
        #c sono tuple naz1id, naz2id
        for c in DAO.getedges(year):
            self._graph.add_edge(self.idMap[c[0]], self.idMap[c[1]])

    def getnodesdegree(self):
        return self._graph.degree()

    def getcompconn(self):
        return len(list(nx.connected_components(self._graph)))

    def compconnstato(self, stato):
        return list(nx.dfs_tree(self._graph, stato))