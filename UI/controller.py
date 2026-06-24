import flet as ft
from networkx.algorithms import chordal

from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        chrom1 = self._view.dd_min_ch.value
        chrom2 = self._view.dd_max_ch.value

        if chrom1 is None:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text("Attenzione, seleziona un valore per il cromosoma minimo!", color="red"))
            self._view.update_page()
            return

        if chrom2 is None:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text("Attenzione, seleziona un valore per il cromosoma massimo!", color="red"))
            self._view.update_page()
            return

        try:
            chrom1Int = int(chrom1)
        except ValueError:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text("Attenzione, seleziona un valore valido per il cromosoma minimo!", color="red"))
            self._view.update_page()
            return

        try:
            chrom2Int = int(chrom2)
        except ValueError:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text("Attenzione, seleziona un valore valido per il cromosoma massimo!", color="red"))
            self._view.update_page()
            return

        if chrom1Int > chrom2Int:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text("Attenzione, il cromosoma minimo non può essere più grande del cromosoma massimo!", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(chrom1Int, chrom2Int)
        nodes, edges = self._model.graphDetails()
        top5nodes = self._model.getTop5Nodes()
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text(f"Creato grafo con {nodes} nodi e {edges} archi"))
        for node in top5nodes:
            self._view.txt_result1.controls.append(ft.Text(f"{node[0]} | num. archi uscenti: {node[1]} | peso tot.: {node[2]}"))
        self._view.update_page()

    def handle_dettagli(self, e):
        pass

    def handle_path(self, e):
        if not self._model.isGraphOk():
            self._view.txt_result2.controls.clear()
            self._view.txt_result2.controls.append(ft.Text("Attenzione, devi creare il grafo prima!", color="red"))
            self._view.update_page()
            return

        bestPath, bestPeso = self._model.bestPath()
        if bestPath is None:
            self._view.txt_result2.controls.clear()
            self._view.txt_result2.controls.append(ft.Text("Non è stato trovato nessun cammino!", color="red"))
            self._view.update_page()
            return

        self._view.txt_result2.controls.clear()
        self._view.txt_result2.controls.append(ft.Text(f"Trovato un cammino ottimo con {len(bestPath)} nodi e peso {bestPeso}."))
        for node in bestPath:
            self._view.txt_result2.controls.append(ft.Text(node))
        self._view.update_page()

    def fillDDChromMin(self):
        allChromes = self._model.getChromosomes()
        chromesOptions = map(lambda x: ft.dropdown.Option(x), allChromes)
        self._view.dd_min_ch.options = chromesOptions
        self._view.update_page()

    def fillDDChromMax(self):
        allChromes = self._model.getChromosomes()
        chromesOptions = map(lambda x: ft.dropdown.Option(x), allChromes)
        self._view.dd_max_ch.options = chromesOptions
        self._view.update_page()