import flet as ft
from datetime import datetime
from models.viagens_controller import ViagensController

db_viagens = ViagensController()
viagens = []

def View(page: ft.Page):
    viagem_para_excluir = {"index": None}
    viagem_em_edicao = {"index": None}

    id_field = ft.TextField(label="ID", read_only=True, width=120)
    id_embarcacao_field = ft.Dropdown(label="Embarcação", options=[], width=200)
    id_porto_origem_field = ft.Dropdown(label="Porto de Origem", options=[], width=200)
    id_porto_destino_field = ft.Dropdown(label="Porto de Destino", options=[], width=200)

    def voltar_home(e):
        page.go("/admin_home")

    def carregar_embarcacoes():
        from models.embarcacoes_controller import EmbarcacoesController
        embarcacoes = EmbarcacoesController().listar_embarcacoes()
        id_embarcacao_field.options = [
            ft.dropdown.Option(text=e["nome"], key=str(e["id"])) for e in embarcacoes
        ]

    def carregar_portos():
        from models.portos_controller import PortosController
        portos = PortosController().listar_portos()
        id_porto_origem_field.options = [
            ft.dropdown.Option(text=f"{p['nome']} - {p['cidade']}/{p['estado']}", key=str(p["id"])) for p in portos
        ]
        id_porto_destino_field.options = id_porto_origem_field.options.copy()

    def criar_linha_tabela(i, v):
        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(v["id"]))),
                ft.DataCell(ft.Text(str(v["id_embarcacao"]))),
                ft.DataCell(ft.Text(str(v["id_porto_origem"]))),
                ft.DataCell(ft.Text(str(v["id_porto_destino"]))),
                ft.DataCell(ft.Text(v["data_partida"])),
                ft.DataCell(
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            tooltip="Editar viagem",
                            icon_color=ft.Colors.BLUE,
                            on_click=lambda e, idx=i: editar_viagem(idx)(e)
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            tooltip="Excluir viagem",
                            icon_color=ft.Colors.RED,
                            on_click=lambda e, idx=i: excluir_viagem(idx)(e)
                        ),
                    ], spacing=5)
                ),
            ]
        )

    def atualizar_lista():
        tabela.rows.clear()
        viagens.clear()
        viagens.extend(db_viagens.listar_viagens())
        for i, v in enumerate(viagens):
            tabela.rows.append(criar_linha_tabela(i, v))
        page.update()

    def editar_viagem(index):
        def handler(e):
            viagem_em_edicao["index"] = index
            viagem = viagens[index]
            id_field.value = viagem["id"]
            id_embarcacao_field.value = str(viagem["id_embarcacao"])
            id_porto_origem_field.value = str(viagem["id_porto_origem"])
            id_porto_destino_field.value = str(viagem["id_porto_destino"])
            data_partida_field.value = viagem["data_partida"]
            dialog.open = True
            page.update()
        return handler

    def excluir_viagem(index):
        def handler(e):
            viagem_para_excluir["index"] = index
            confirm_dialog.open = True
            page.update()
        return handler

    def confirmar_exclusao(e):
        index = viagem_para_excluir["index"]
        if index is not None:
            viagem_id = viagens[index]["id"]
            if db_viagens.excluir_viagem(viagem_id):
                viagens.pop(index)
                atualizar_lista()
        confirm_dialog.open = False
        page.update()

    def cancelar_exclusao(e):
        confirm_dialog.open = False
        page.update()

    def limpar_campos():
        id_field.value = ""
        id_embarcacao_field.value = ""
        id_porto_origem_field.value = ""
        id_porto_destino_field.value = ""
        data_partida_field.value = ""
        viagem_em_edicao["index"] = None
        for f in [id_embarcacao_field, id_porto_origem_field, id_porto_destino_field, data_partida_field]:
            f.error_text = None
            f.border_color = None

    def salvar_viagem_click(e):
        campos_obrigatorios = [
            (id_embarcacao_field, "Embarcação"),
            (id_porto_origem_field, "Porto de Origem"),
            (id_porto_destino_field, "Porto de Destino"),
            (data_partida_field, "Data de Partida")
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

        try:
            datetime.strptime(data_partida_field.value, "%Y-%m-%d")
        except ValueError:
            data_partida_field.error_text = "Formato de data inválido (AAAA-MM-DD)"
            data_partida_field.border_color = ft.Colors.RED_400
            page.update()
            return

        nova_viagem = {
            "id_embarcacao": int(id_embarcacao_field.value),
            "id_porto_origem": int(id_porto_origem_field.value),
            "id_porto_destino": int(id_porto_destino_field.value),
            "data_partida": data_partida_field.value
        }

        if viagem_em_edicao["index"] is None:
            viagem_id = db_viagens.cadastrar_viagem(nova_viagem)
            if viagem_id:
                nova_viagem["id"] = viagem_id
                viagens.append(nova_viagem)
        else:
            index = viagem_em_edicao["index"]
            viagem_id = viagens[index]["id"]
            if db_viagens.atualizar_viagem(viagem_id, nova_viagem):
                nova_viagem["id"] = viagem_id
                viagens[viagem_em_edicao["index"]] = nova_viagem

        viagem_em_edicao["index"] = None
        atualizar_lista()
        dialog.open = False
        page.update()

    salvar_viagem = ft.ElevatedButton(
        "Salvar",
        on_click=salvar_viagem_click,
        tooltip="Salvar viagem",
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.GREEN,
            color=ft.Colors.WHITE,
        )
    )

    data_partida_field = ft.TextField(
        label="* Data de Partida (AAAA-MM-DD)",
        hint_text="Ex: 2025-12-31"
    )

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Cadastrar/Editar Viagem"),
        content=ft.Container(
            content=ft.Column([
                ft.Row([id_field, id_embarcacao_field], spacing=10),
                ft.Row([id_porto_origem_field, id_porto_destino_field], spacing=10),
                data_partida_field
            ], tight=True, scroll=ft.ScrollMode.AUTO),
            width=450,
            height=300,
            padding=10
        ),
        actions=[
            salvar_viagem,
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
        content=ft.Text("Você realmente deseja excluir esta viagem?"),
        actions=[
            ft.TextButton("Cancelar", on_click=cancelar_exclusao),
            ft.TextButton("Excluir", on_click=confirmar_exclusao),
        ]
    )
    page.overlay.append(confirm_dialog)

    campo_pesquisa = ft.TextField(
        label="Pesquisar viagem (por data ou ID)",
        visible=True,
        on_change=lambda e: filtrar_viagens(e.control.value),
        prefix_icon=ft.Icons.SEARCH,
        width=500
    )

    def filtrar_viagens(query):
        tabela.rows.clear()
        for i, v in enumerate(viagens):
            if (
                query in v["data_partida"]
                or query == str(v["id"])
            ):
                tabela.rows.append(criar_linha_tabela(i, v))
        page.update()

    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("EMBARCAÇÃO")),
            ft.DataColumn(ft.Text("ORIGEM")),
            ft.DataColumn(ft.Text("DESTINO")),
            ft.DataColumn(ft.Text("DATA")),
            ft.DataColumn(ft.Text("AÇÕES")),
        ],
        rows=[]
    )

    carregar_embarcacoes()
    carregar_portos()
    atualizar_lista()

    def abrir_dialogo_cadastro(e):
        viagem_em_edicao["index"] = None
        limpar_campos()
        dialog.open = True
        page.update()

    return ft.View(
        route="/viagens",
        appbar=ft.AppBar(
            title=ft.Row([
                ft.Icon(name=ft.Icons.DIRECTIONS_BOAT, color=ft.Colors.WHITE),
                ft.Text("Viagens", color=ft.Colors.WHITE),
            ], spacing=10),
            leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, tooltip="Voltar", icon_color=ft.Colors.WHITE, on_click=voltar_home),
            bgcolor=ft.Colors.INDIGO
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
                            bgcolor=ft.Colors.INDIGO,
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