import flet as ft
from models.passagens_controller import PassagensController

db_passagens = PassagensController()
passagens = []

def View(page: ft.Page):
    passagem_para_excluir = {"index": None}
    passagem_em_edicao = {"index": None}

    id_field = ft.TextField(label="ID", read_only=True, width=120)
    id_viagem_field = ft.Dropdown(label="Viagem", options=[], width=200)
    id_assento_field = ft.Dropdown(label="Assento", options=[], width=200)
    id_passageiro_field = ft.Dropdown(label="Passageiro", options=[], width=200)

    def voltar_home(e):
        page.go("/admin_home")

    def carregar_viagens():
        from models.viagens_controller import ViagensController
        viagens = ViagensController().listar_viagens()
        id_viagem_field.options = [
            ft.dropdown.Option(text=f"Viagem {v['id']} - {v['data_partida']}", key=str(v["id"])) for v in viagens
        ]

    def carregar_assentos():
        from models.assentos_controller import AssentosController
        assentos = AssentosController().listar_assentos()
        id_assento_field.options = [
            ft.dropdown.Option(text=f"Assento {a['numero_assento']} (Emb. {a['id_embarcacao']})", key=str(a["id"])) for a in assentos
        ]

    def carregar_passageiros():
        from models.passageiros_controller import PassageirosController
        passageiros = PassageirosController().listar_passageiros()
        id_passageiro_field.options = [
            ft.dropdown.Option(text=p["nome"], key=str(p["id"])) for p in passageiros
        ]

    def criar_linha_tabela(i, p):
        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(p["id"]))),
                ft.DataCell(ft.Text(str(p["id_viagem"]))),
                ft.DataCell(ft.Text(str(p["id_assento"]))),
                ft.DataCell(ft.Text(str(p["id_passageiro"]))),
                ft.DataCell(
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            tooltip="Editar passagem",
                            icon_color=ft.Colors.BLUE,
                            on_click=lambda e, idx=i: editar_passagem(idx)(e)
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            tooltip="Excluir passagem",
                            icon_color=ft.Colors.RED,
                            on_click=lambda e, idx=i: excluir_passagem(idx)(e)
                        ),
                    ], spacing=5)
                ),
            ]
        )

    def atualizar_lista():
        tabela.rows.clear()
        passagens.clear()
        passagens.extend(db_passagens.listar_passagens())
        for i, p in enumerate(passagens):
            tabela.rows.append(criar_linha_tabela(i, p))
        page.update()

    def editar_passagem(index):
        def handler(e):
            passagem_em_edicao["index"] = index
            passagem = passagens[index]
            id_field.value = passagem["id"]
            id_viagem_field.value = str(passagem["id_viagem"])
            id_assento_field.value = str(passagem["id_assento"])
            id_passageiro_field.value = str(passagem["id_passageiro"])
            dialog.open = True
            page.update()
        return handler

    def excluir_passagem(index):
        def handler(e):
            passagem_para_excluir["index"] = index
            confirm_dialog.open = True
            page.update()
        return handler

    def confirmar_exclusao(e):
        index = passagem_para_excluir["index"]
        if index is not None:
            passagem_id = passagens[index]["id"]
            if db_passagens.excluir_passagem(passagem_id):
                passagens.pop(index)
                atualizar_lista()
        confirm_dialog.open = False
        page.update()

    def cancelar_exclusao(e):
        confirm_dialog.open = False
        page.update()

    def limpar_campos():
        id_field.value = ""
        id_viagem_field.value = ""
        id_assento_field.value = ""
        id_passageiro_field.value = ""
        passagem_em_edicao["index"] = None
        for f in [id_viagem_field, id_assento_field, id_passageiro_field]:
            f.error_text = None
            f.border_color = None

    def salvar_passagem_click(e):
        campos_obrigatorios = [
            (id_viagem_field, "Viagem"),
            (id_assento_field, "Assento"),
            (id_passageiro_field, "Passageiro")
        ]
        faltando = False
        for campo, nome in campos_obrigatorios:
            if not campo.value:
                campo.error_text = f"* {nome} obrigatório"
                campo.border_color = ft.Colors.RED_400
                faltando = True
            else:
                campo.error_text = None
                campo.border_color = None

        if faltando:
            page.update()
            return

        nova_passagem = {
            "id_viagem": int(id_viagem_field.value),
            "id_assento": int(id_assento_field.value),
            "id_passageiro": int(id_passageiro_field.value)
        }

        if passagem_em_edicao["index"] is None:
            passagem_id = db_passagens.cadastrar_passagem(nova_passagem)
            if passagem_id:
                nova_passagem["id"] = passagem_id
                passagens.append(nova_passagem)
        else:
            index = passagem_em_edicao["index"]
            passagem_id = passagens[index]["id"]
            if db_passagens.atualizar_passagem(passagem_id, nova_passagem):
                nova_passagem["id"] = passagem_id
                passagens[passagem_em_edicao["index"]] = nova_passagem

        passagem_em_edicao["index"] = None
        atualizar_lista()
        dialog.open = False
        page.update()

    salvar_passagem = ft.ElevatedButton(
        "Salvar",
        on_click=salvar_passagem_click,
        tooltip="Salvar passagem",
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.GREEN,
            color=ft.Colors.WHITE,
        )
    )

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Cadastrar/Editar Passagem"),
        content=ft.Container(
            content=ft.Column([
                ft.Row([id_field, id_viagem_field], spacing=10),
                ft.Row([id_assento_field, id_passageiro_field], spacing=10),
            ], tight=True, scroll=ft.ScrollMode.AUTO),
            width=450,
            height=250,
            padding=10
        ),
        actions=[
            salvar_passagem,
            ft.ElevatedButton(
                "Cancelar",
                tooltip="Cancelar operação",
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.RED,
                    color=ft.Colors.WHITE,
                ),
                on_click=lambda e: (
                    setattr(dialog, 'open', False),
                    page.update()
                )
            ),
        ]
    )
    page.overlay.append(dialog)

    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Exclusão"),
        content=ft.Text("Você realmente deseja excluir esta passagem?"),
        actions=[
            ft.TextButton("Cancelar", on_click=cancelar_exclusao),
            ft.TextButton("Excluir", on_click=confirmar_exclusao),
        ]
    )
    page.overlay.append(confirm_dialog)

    campo_pesquisa = ft.TextField(
        label="Pesquisar passagem (por ID)",
        visible=True,
        on_change=lambda e: filtrar_passagens(e.control.value),
        prefix_icon=ft.Icons.SEARCH,
        width=500
    )
    

    def filtrar_passagens(query):
        tabela.rows.clear()
        for i, p in enumerate(passagens):
            if query == str(p["id"]):
                tabela.rows.append(criar_linha_tabela(i, p))
        page.update()

    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("VIAGEM")),
            ft.DataColumn(ft.Text("ASSENTO")),
            ft.DataColumn(ft.Text("PASSAGEIRO")),
            ft.DataColumn(ft.Text("AÇÕES")),
        ],
        rows=[]
    )

    carregar_viagens()
    carregar_assentos()
    carregar_passageiros()
    atualizar_lista()

    def abrir_dialogo_cadastro(e):
        passagem_em_edicao["index"] = None
        limpar_campos()
        dialog.open = True
        page.update()

    return ft.View(
        route="/passagens",
        appbar=ft.AppBar(
            title=ft.Row([
                ft.Icon(name=ft.Icons.CONFIRMATION_NUMBER, color=ft.Colors.WHITE),
                ft.Text("Passagens", color=ft.Colors.WHITE),
            ], spacing=10),
            leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, tooltip="Voltar", icon_color=ft.Colors.WHITE, on_click=voltar_home),
            bgcolor=ft.Colors.DEEP_ORANGE
        ),
        controls=[
            ft.Stack(
                controls=[
                    ft.Column(
                        controls=[
                            campo_pesquisa, ft.Divider(),
                            tabela, ft.Divider()
                        ],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True
                    ),
                    ft.Container(
                        content=ft.FloatingActionButton(
                            text="Cadastrar",
                            icon=ft.Icons.ADD,
                            on_click=abrir_dialogo_cadastro,
                            bgcolor=ft.Colors.DEEP_ORANGE,
                            foreground_color=ft.Colors.WHITE
                        ),
                        left=20,
                        bottom=20,
                        alignment=ft.alignment.bottom_left
                    )
                ],
                expand=True
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.START
    )