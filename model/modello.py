import networkx as nx
from markdown_it import parser_inline

from database.DAO import DAO
import copy

class Model:

    def __init__(self):
        self._idMapGenes = {}
        genes = DAO.get_all_genes()
        for gene in genes:
            self._idMapGenes[(gene.GeneID, gene.Function)] = gene
        self._graph = nx.DiGraph()
        self._bestPaths = []
        self._bestLun = 0

    def bestPath(self):
        self._bestPaths = []
        self._bestLun = 0
        parziale = []
        for node in self._graph.nodes:
            parziale.append(node)
            self._ricorsione(parziale)
            parziale.pop()
        pathWMaxLun = []
        for path in self._bestPaths:
            if len(path) == self._bestLun:
                pathWMaxLun.append(path)
        if len(pathWMaxLun) == 0:
            return None, None
        elif len(pathWMaxLun) == 1:
            bestScore = self._getScore(pathWMaxLun[0])
            return pathWMaxLun[0], bestScore
        else:
            bestPath, bestScore = self._computeBestPath(pathWMaxLun)
            return bestPath, bestScore

    def _ricorsione(self, parziale):
        # Condizione di ottimalità
        if len(parziale) > self._bestLun:
            self._bestLun = len(parziale)
            self._bestPaths.append(copy.deepcopy(parziale))

        # Ricorsione
        for v in self._graph.neighbors(parziale[-1]):
            if v not in parziale and v.Essential != parziale[-1].Essential:
                if len(parziale) < 2:
                    parziale.append(v)
                    self._ricorsione(parziale)
                    parziale.pop()
                else:
                    if self._graph[parziale[-2]][parziale[-1]]['weight'] <= self._graph[parziale[-1]][v]['weight']:
                        parziale.append(v)
                        self._ricorsione(parziale)
                        parziale.pop()

    def _getScore(self, path):
        sommaPesi = 0
        for i in range(len(path) - 1):
            sommaPesi += self._graph[path[i]][path[i + 1]]['weight']
        return sommaPesi

    def _computeBestPath(self, pathWMaxLun):
        bestScore = 1000000
        bestPath = []
        for path in pathWMaxLun:
            score = self._getScore(path)
            if score < bestScore:
                bestScore = score
                bestPath = path
        return bestPath, bestScore

    def buildGraph(self, chromMin, chromMax):
        self._graph.clear()
        genes = DAO.getAllGenesByChrom(chromMin, chromMax)
        self._graph.add_nodes_from(genes)
        edges = DAO.getAllEdges(chromMin, chromMax)
        for edge in edges:
            peso = edge[4]
            crom1 = self._idMapGenes[(edge[0], edge[1])]
            crom2 = self._idMapGenes[(edge[2], edge[3])]
            if crom1.Chromosome == crom2.Chromosome:
                self._graph.add_edge(crom1, crom2, weight=peso)
                self._graph.add_edge(crom2, crom1, weight=peso)
            elif crom1.Chromosome > crom2.Chromosome:
                self._graph.add_edge(crom2, crom1, weight=peso)
            else:
                self._graph.add_edge(crom1, crom2, weight=peso)

    def graphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    @staticmethod
    def getChromosomes():
        return DAO.getAllChrom()

    def getTop5Nodes(self):
        archi = []
        for node in self._graph.nodes:
            succs = self._graph.successors(node)
            pesoTot = 0
            succsNum = 0
            for suc in succs:
                pesoTot += self._graph[node][suc]['weight']
                succsNum += 1
            archi.append((node, succsNum, pesoTot))
        return sorted(archi, key=lambda x: x[1], reverse=True)[:5]

    def isGraphOk(self):
        return len(self._graph.nodes) > 0 and len(self._graph.edges) > 0