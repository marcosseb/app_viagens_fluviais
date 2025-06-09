import flet as ft
from models.assentos_controller import AssentosController
from models.embarcacoes_controller import EmbarcacoesController

db_assentos = AssentosController()
assentos = []

def View(page: ft.Page):
    assento_para_excluir = {"index": None}
    assento_em_edicao = {"index": None}

    id_field = ft.TextField(label="ID", read_only=True, width=120)
    id_embarcacao_field = ft.Dropdown(label="Embarcação", options=[], width=180)

    def voltar_home(e):
        page.go("/admin_home")

    def carregar_embarcacoes():
        embarcacoes = EmbarcacoesController().listar_embarcacoes()
        id_embarcacao_field.options = [
            ft.dropdown.Option(text=e["nome"], key=str(e["id"])) for e in embarcacoes
        ]

    def criar_linha_tabela(i, a):
        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(a["id"]))),
                ft.DataCell(ft.Text(str(a["id_embarcacao"]))),
                ft.DataCell(ft.Text(str(a["numero_assento"]))),
                ft.DataCell(ft.Text(a["tipo"])),
                ft.DataCell(
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            tooltip="Editar assento",
                            icon_color=ft.Colors.BLUE,
                            on_click=lambda e, idx=i: editar_assento(idx)(e)
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            tooltip="Excluir assento",
                            icon_color=ft.Colors.RED,
                            on_click=lambda e, idx=i: excluir_assento(idx)(e)
                        ),
                    ], spacing=5)
                ),
            ]
        )

    def atualizar_lista():
        tabela.rows.clear()
        assentos.clear()
        assentos.extend(db_assentos.listar_assentos())
        for i, a in enumerate(assentos):
            tabela.rows.append(criar_linha_tabela(i, a))
        page.update()

    def editar_assento(index):
        def handler(e):
            assento_em_edicao["index"] = index
            assento = assentos[index]
            id_field.value = assento["id"]
            id_embarcacao_field.value = str(assento["id_embarcacao"])
            numero_assento_field.value = str(assento["numero_assento"])
            tipo_field.value = assento["tipo"]
            dialog.open = True
            page.update()
        return handler

    def excluir_assento(index):
        def handler(e):
            assento_para_excluir["index"] = index
            confirm_dialog.open = True
            page.update()
        return handler

    def confirmar_exclusao(e):
        index = assento_para_excluir["index"]
        if index is not None:
            assento_id = assentos[index]["id"]
            if db_assentos.excluir_assento(assento_id):
                assentos.pop(index)
                atualizar_lista()
        confirm_dialog.open = False
        page.update()

    def cancelar_exclusao(e):
        confirm_dialog.open = False
        page.update()

    def limpar_campos():
        id_field.value = ""
        id_embarcacao_field.value = ""
        numero_assento_field.value = ""
        tipo_field.value = ""
        assento_em_edicao["index"] = None
        for f in [id_embarcacao_field, numero_assento_field, tipo_field]:
            f.error_text = None
            f.border_color = None

    def salvar_assento_click(e):
        campos_obrigatorios = [
            (id_embarcacao_field, "Embarcação"),
            (numero_assento_field, "Número do Assento"),
            (tipo_field, "Tipo")
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

        novo_assento = {
            "id_embarcacao": int(id_embarcacao_field.value),
            "numero_assento": int(numero_assento_field.value),
            "tipo": tipo_field.value
        }

        if assento_em_edicao["index"] is None:
            assento_id = db_assentos.cadastrar_assento(novo_assento)
            if assento_id:
                novo_assento["id"] = assento_id
                assentos.append(novo_assento)
        else:
            index = assento_em_edicao["index"]
            assento_id = assentos[index]["id"]
            if db_assentos.atualizar_assento(assento_id, novo_assento):
                novo_assento["id"] = assento_id
                assentos[assento_em_edicao["index"]] = novo_assento

        assento_em_edicao["index"] = None
        atualizar_lista()
        dialog.open = False
        page.update()

    salvar_assento = ft.ElevatedButton(
        "Salvar",
        on_click=salvar_assento_click,
        tooltip="Salvar assento",
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.GREEN,
            color=ft.Colors.WHITE,
        )
    )

    numero_assento_field = ft.TextField(label="* Número do Assento")
    tipo_field = ft.Dropdown(
        label="* Tipo",
        options=[
            ft.dropdown.Option("Normal"),
            ft.dropdown.Option("VIP"),
            ft.dropdown.Option("Deficiente")
        ]
    )

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Cadastrar/Editar Assento"),
        content=ft.Container(
            content=ft.Column([
                ft.Row([id_field, id_embarcacao_field], spacing=10),
                numero_assento_field,
                tipo_field
            ], tight=True, scroll=ft.ScrollMode.AUTO),
            width=350,
            height=300,
            padding=10
        ),
        actions=[
            salvar_assento,
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
        content=ft.Text("Você realmente deseja excluir este assento?"),
        actions=[
            ft.TextButton("Cancelar", on_click=cancelar_exclusao),
            ft.TextButton("Excluir", on_click=confirmar_exclusao),
        ]
    )
    page.overlay.append(confirm_dialog)

    campo_pesquisa = ft.TextField(
        label="Pesquisar assento (por número ou ID)",
        visible=True,
        on_change=lambda e: filtrar_assentos(e.control.value),
        prefix_icon=ft.Icons.SEARCH,
        width=500
    )

    def filtrar_assentos(query):
        tabela.rows.clear()
        for i, a in enumerate(assentos):
            if (
                query == str(a["numero_assento"])
                or query == str(a["id"])
            ):
                tabela.rows.append(criar_linha_tabela(i, a))
        page.update()

    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("EMBARCAÇÃO")),
            ft.DataColumn(ft.Text("NÚMERO")),
            ft.DataColumn(ft.Text("TIPO")),
            ft.DataColumn(ft.Text("AÇÕES")),
        ],
        rows=[]
    )

    carregar_embarcacoes()
    atualizar_lista()

    def abrir_dialogo_cadastro(e):
        assento_em_edicao["index"] = None
        limpar_campos()
        dialog.open = True
        page.update()

    return ft.View(
        route="/assentos",
        appbar=ft.AppBar(
            title=ft.Row([
                ft.Icon(name=ft.Icons.EVENT_SEAT, color=ft.Colors.WHITE),
                ft.Text("Assentos", color=ft.Colors.WHITE),
            ], spacing=10),
            leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, tooltip="Voltar", icon_color=ft.Colors.WHITE, on_click=voltar_home),
            bgcolor=ft.Colors.PURPLE
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
                            bgcolor=ft.Colors.PURPLE,
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