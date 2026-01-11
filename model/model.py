from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):

        self.G = nx.DiGraph()
        self.geni = DAO.get_geni()
        self.interazioni=DAO.get_interazioni()


    def build_weighted_graph(self):
        cromosomi = set()
        for g in self.geni.values():
            if g.cromosoma != 0:
                cromosomi.add(g.cromosoma)

        self.G.add_nodes_from(cromosomi)

        coppie_viste = set()

        for i in self.interazioni:
            if i.id_gene1 not in self.geni or i.id_gene2 not in self.geni:
                continue

            g1 = self.geni[i.id_gene1]
            g2 = self.geni[i.id_gene2]

            if g1.cromosoma == 0 or g2.cromosoma == 0 or g1.cromosoma == g2.cromosoma:
                continue

            coppia = (i.id_gene1, i.id_gene2)
            if coppia in coppie_viste:
                continue
            coppie_viste.add(coppia)

            c1 = g1.cromosoma
            c2 = g2.cromosoma

            if self.G.has_edge(c1, c2):
                self.G[c1][c2]["weight"] += i.correlazione
            else:
                self.G.add_edge(c1, c2, weight=i.correlazione)

    def number_of_nodes(self):
        return self.G.number_of_nodes()

    def number_of_edges(self):
        return self.G.number_of_edges()

    def get_edges_weight_min_max(self):

        pesi = nx.get_edge_attributes(self.G, 'weight')
        if pesi:
            valori = pesi.values()
            pesi_minimi= min(valori)
            pesi_massimi= max(valori)

        return pesi_minimi,pesi_massimi

    def count_edges(self, soglia):

        pesi = nx.get_edge_attributes(self.G, 'weight')
        minori = []
        maggiori = []

        if pesi:
            valori = pesi.values()
            for i in valori:
                if i <= soglia:
                    minori.append(i)
                elif i >= soglia:
                    maggiori.append(i)

        return len(minori), len(maggiori)

    def find_best_path(self, S):
        self.best_path = []
        self.best_cost = 0

        for nodo in self.G.nodes:
            self._ricorsione(nodo, [nodo], 0, S)

        return self.best_path, self.best_cost

    def _ricorsione(self, current, path, cost, S):
        if cost> self.best_cost:

            self.best_cost = cost
            self.best_path=path.copy()

        for vicino in self.G.neighbors(current):
            peso = self.G[current][vicino]["weight"]

            if peso > S and vicino not in path:
                path.append(vicino)
                self._ricorsione(vicino, path, cost + peso, S)
                path.pop()



