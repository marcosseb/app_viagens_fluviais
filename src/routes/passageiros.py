import flet as ft
from models.passageiros_controller import PassageirosController

db_passageiros = PassageirosController()
passageiros = []

def View(page: ft.Page):
    passageiro_para_excluir = {"index": None}
    passageiro_em_edicao = {"index": None}

    id_field = ft.TextField(label="ID", read_only=True, width=120)

    def voltar_home(e):
        page.go("/admin_home")

    def criar_linha_tabela(i, p):
        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(p["id"]))),
                ft.DataCell(ft.Text(p["nome"], max_lines=2, overflow=ft.TextOverflow.ELLIPSIS)),
                ft.DataCell(
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            tooltip="Editar passageiro",
                            icon_color=ft.Colors.BLUE,
                            on_click=lambda e, idx=i: editar_passageiro(idx)(e)
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            tooltip="Excluir passageiro",
                            icon_color=ft.Colors.RED,
                            on_click=lambda e, idx=i: excluir_passageiro(idx)(e)
                        ),
                    ], spacing=5)
                ),
            ]
        )

    def atualizar_lista():
        tabela.rows.clear()
        passageiros.clear()
        passageiros.extend(db_passageiros.listar_passageiros())
        for i, p in enumerate(passageiros):
            tabela.rows.append(criar_linha_tabela(i, p))
        page.update()

    def editar_passageiro(index):
        def handler(e):
            passageiro_em_edicao["index"] = index
            passageiro = passageiros[index]
            id_field.value = passageiro["id"]
            nome_field.value = passageiro["nome"]
            dialog.open = True
            page.update()
        return handler

    def excluir_passageiro(index):
        def handler(e):
            passageiro_para_excluir["index"] = index
            confirm_dialog.open = True
            page.update()
        return handler

    def confirmar_exclusao(e):
        index = passageiro_para_excluir["index"]
        if index is not None:
            passageiro_id = passageiros[index]["id"]
            if db_passageiros.excluir_passageiro(passageiro_id):
                passageiros.pop(index)
                atualizar_lista()
        confirm_dialog.open = False
        page.update()

    def cancelar_exclusao(e):
        confirm_dialog.open = False
        page.update()

    def limpar_campos():
        id_field.value = ""
        nome_field.value = ""
        passageiro_em_edicao["index"] = None
        nome_field.error_text = None
        nome_field.border_color = None

    def salvar_passageiro_click(e):
        if not nome_field.value:
            nome_field.error_text = "* Nome obrigatório"
            nome_field.border_color = ft.Colors.RED_400
            page.update()
            return

        novo_passageiro = {
            "nome": nome_field.value
        }

        if passageiro_em_edicao["index"] is None:
            passageiro_id = db_passageiros.cadastrar_passageiro(novo_passageiro)
            if passageiro_id:
                novo_passageiro["id"] = passageiro_id
                passageiros.append(novo_passageiro)
        else:
            index = passageiro_em_edicao["index"]
            passageiro_id = passageiros[index]["id"]
            if db_passageiros.atualizar_passageiro(passageiro_id, novo_passageiro):
                novo_passageiro["id"] = passageiro_id
                passageiros[passageiro_em_edicao["index"]] = novo_passageiro

        passageiro_em_edicao["index"] = None
        atualizar_lista()
        dialog.open = False
        page.update()

    salvar_passageiro = ft.ElevatedButton(
        "Salvar",
        on_click=salvar_passageiro_click,
        tooltip="Salvar passageiro",
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.GREEN,
            color=ft.Colors.WHITE,
        )
    )

    nome_field = ft.TextField(label="* Nome", width=300)

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Cadastrar/Editar Passageiro"),
        content=ft.Container(
            content=ft.Column([
                ft.Row([id_field, nome_field], spacing=10),
            ], tight=True, scroll=ft.ScrollMode.AUTO),
            width=350,
            height=200,
            padding=10
        ),
        actions=[
            salvar_passageiro,
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
        content=ft.Text("Você realmente deseja excluir este passageiro?"),
        actions=[
            ft.TextButton("Cancelar", on_click=cancelar_exclusao),
            ft.TextButton("Excluir", on_click=confirmar_exclusao),
        ]
    )
    page.overlay.append(confirm_dialog)

    campo_pesquisa = ft.TextField(
        label="Pesquisar passageiro (por nome ou ID)",
        visible=True,
        on_change=lambda e: filtrar_passageiros(e.control.value),
        prefix_icon=ft.Icons.SEARCH,
        width=500
    )

    def filtrar_passageiros(query):
        tabela.rows.clear()
        for i, p in enumerate(passageiros):
            if (
                query.lower() in p["nome"].lower()
                or query == str(p["id"])
            ):
                tabela.rows.append(criar_linha_tabela(i, p))
        page.update()

    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("NOME")),
            ft.DataColumn(ft.Text("AÇÕES")),
        ],
        rows=[]
    )

    atualizar_lista()

    def abrir_dialogo_cadastro(e):
        passageiro_em_edicao["index"] = None
        limpar_campos()
        dialog.open = True
        page.update()

    return ft.View(
        route="/passageiros",
        appbar=ft.AppBar(
            title=ft.Row([
                ft.Icon(name=ft.Icons.PERSON, color=ft.Colors.WHITE),
                ft.Text("Passageiros", color=ft.Colors.WHITE),
            ], spacing=10),
            leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, tooltip="Voltar", icon_color=ft.Colors.WHITE, on_click=voltar_home),
            bgcolor=ft.Colors.TEAL
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
                            bgcolor=ft.Colors.TEAL,
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