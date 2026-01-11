import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """""
        # TODO
        self._model.build_weighted_graph()
        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(
            ft.Text(f"Grafo calcolato: {self._model.G.number_of_nodes()} nodi, {self._model.G.number_of_edges()} archi"))
        min_p, max_p = self._model.get_edges_weight_min_max()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Peso min: {min_p:.2f}, Peso max: {max_p:.2f}"))
        self._view.page.update()


    def handle_conta_edges(self, e):
        """ Handler per gestire il conteggio degli archi """""
        # TODO
        try:
            soglia = float(self._view.txt_name.value)
        except:
            self._view.show_alert("Inserisci un numero valido per la soglia.")
            return

        if soglia < 3 or soglia > 7:
            self._view.show_alert(f"Soglia fuori range ({3}-{7})")
            return

        minori, maggiori = self._model.count_edges(soglia)
        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Archi < {soglia}: {minori}"))
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f" Archi > {soglia}: {maggiori}"))

        self._view.page.update()

    def handle_ricerca(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """""
        # TODO
        soglia = float(self._view.txt_name.value)

        sequenza, costo = self._model.find_best_path(soglia)
        self._view.lista_visualizzazione_3.controls.clear()
        self._view.lista_visualizzazione_3.controls.append(ft.Text(f" {sequenza}: {costo:.2f}"))

        self._view.page.update()