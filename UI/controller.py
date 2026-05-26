import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._Statopartenza = None

    def handleCalcola(self, e):
        annoinserito = self._view._txtAnno.value
        if annoinserito == "" or annoinserito is None or not annoinserito.isdigit():
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Devi inserire un anno valido", color="red", size=18))
            self._view.update_page()
            return
        if int(annoinserito) < 1816 or int(annoinserito) > 2006:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text("L'anno inserito deve essere nel'intervallo 1816-2006", color="red", size=18))
            self._view.update_page()
            return
        self.caricamento()
        self._model.creategraph(annoinserito)
        numcompconn = self._model.getcompconn()
        nodigradi = list(self._model.getnodesdegree())
        nodigradi.sort(key=lambda x: x[0].StateNme)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato", color="green", size=18))
        self._view._txt_result.controls.append(ft.Text(f"Il grafo ha {numcompconn} componenti connesse"))
        for n in nodigradi:
            self._view._txt_result.controls.append(ft.Text(f"{n[0]} -- {n[1]} vicini"))

        self._view._dpdStato.disabled=False
        self._view._btnRaggiungibili.disabled=False
        self.fillDD()
        self._view.update_page()



    def caricamento(self):
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text("Caricamento..."))
        self._view.update_page()

    def handleRaggiungibili(self, e):
        stato = self._Statopartenza
        if stato is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Devi selezionare uno stato", color="red", size=18))
            self._view.update_page()
            return

        self.caricamento()
        stati = self._model.compconnstato(stato)
        stati.sort(key=lambda x: x.StateNme)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text("Componente connessa", color="green", size=18))
        for s in stati:
            self._view._txt_result.controls.append(ft.Text(f"{s}"))

        self._view.update_page()

    def fillDD(self):
        nodi = list(self._model._nodes)
        nodi.sort(key=lambda x: x.StateNme)
        for n in nodi:
            self._view._dpdStato.options.append(ft.dropdown.Option(text=n.StateNme,
                                             data=n,
                                             on_click=self.read_DD_Stato))

    def read_DD_Stato(self, e):
        if e.control.data is None:
            self._Statopartenza = None
        else:
            self._Statopartenza = e.control.data