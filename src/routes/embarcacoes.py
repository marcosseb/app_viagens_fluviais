import flet as ft
from models.embarcacoes_controller import EmbarcacoesController

db_embarcacoes = EmbarcacoesController()
embarcacoes = []

def View(page: ft.Page):
    embarcacao_para_excluir = {"index": None}
    embarcacao_em_edicao = {"index": None}

    id_field = ft.TextField(label="ID", read_only=True, width=120)

    def voltar_home(e):
        page.go("/admin_home")

    def criar_linha_tabela(i, e):
        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(e["id"]))),
                ft.DataCell(ft.Text(e["nome"], max_lines=2, overflow=ft.TextOverflow.ELLIPSIS)),
                ft.DataCell(ft.Text(str(e["capacidade"]))),
                ft.DataCell(
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            tooltip="Editar embarcação",
                            icon_color=ft.Colors.BLUE,
                            on_click=lambda e, idx=i: editar_embarcacao(idx)(e)
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            tooltip="Excluir embarcação",
                            icon_color=ft.Colors.RED,
                            on_click=lambda e, idx=i: excluir_embarcacao(idx)(e)
                        ),
                    ], spacing=5)
                ),
            ]
        )

    def atualizar_lista():
        tabela.rows.clear()
        embarcacoes.clear()
        embarcacoes.extend(db_embarcacoes.listar_embarcacoes())
        for i, e in enumerate(embarcacoes):
            tabela.rows.append(criar_linha_tabela(i, e))
        page.update()

    def editar_embarcacao(index):
        def handler(e):
            embarcacao_em_edicao["index"] = index
            embarcacao = embarcacoes[index]
            id_field.value = embarcacao["id"]
            nome_field.value = embarcacao["nome"]
            capacidade_field.value = str(embarcacao["capacidade"])
            dialog.open = True
            page.update()
        return handler

    def excluir_embarcacao(index):
        def handler(e):
            embarcacao_para_excluir["index"] = index
            confirm_dialog.open = True
            page.update()
        return handler

    def confirmar_exclusao(e):
        index = embarcacao_para_excluir["index"]
        if index is not None:
            embarcacao_id = embarcacoes[index]["id"]
            if db_embarcacoes.excluir_embarcacao(embarcacao_id):
                embarcacoes.pop(index)
                atualizar_lista()
        confirm_dialog.open = False
        page.update()

    def cancelar_exclusao(e):
        confirm_dialog.open = False
        page.update()

    def limpar_campos():
        id_field.value = ""
        nome_field.value = ""
        capacidade_field.value = ""
        embarcacao_em_edicao["index"] = None
        for f in [nome_field, capacidade_field]:
            f.error_text = None
            f.border_color = None

    def salvar_embarcacao_click(e):
        campos_obrigatorios = [
            (nome_field, "Nome"),
            (capacidade_field, "Capacidade")
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
            capacidade = int(capacidade_field.value)
        except ValueError:
            capacidade_field.error_text = "Capacidade deve ser um número"
            capacidade_field.border_color = ft.Colors.RED_400
            page.update()
            return

        nova_embarcacao = {
            "nome": nome_field.value,
            "capacidade": capacidade
        }

        if embarcacao_em_edicao["index"] is None:
            embarcacao_id = db_embarcacoes.cadastrar_embarcacao(nova_embarcacao)
            if embarcacao_id:
                nova_embarcacao["id"] = embarcacao_id
                embarcacoes.append(nova_embarcacao)
        else:
            index = embarcacao_em_edicao["index"]
            embarcacao_id = embarcacoes[index]["id"]
            if db_embarcacoes.atualizar_embarcacao(embarcacao_id, nova_embarcacao):
                nova_embarcacao["id"] = embarcacao_id
                embarcacoes[embarcacao_em_edicao["index"]] = nova_embarcacao

        embarcacao_em_edicao["index"] = None
        atualizar_lista()
        dialog.open = False
        page.update()

    salvar_embarcacao = ft.ElevatedButton(
        "Salvar",
        on_click=salvar_embarcacao_click,
        tooltip="Salvar embarcação",
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.GREEN,
            color=ft.Colors.WHITE,
        )
    )

    nome_field = ft.TextField(label="* Nome", width=180)
    capacidade_field = ft.TextField(label="* Capacidade")

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Cadastrar/Editar Embarcação"),
        content=ft.Container(
            content=ft.Column([
                ft.Row([id_field, nome_field], spacing=10),
                capacidade_field
            ], tight=True, scroll=ft.ScrollMode.AUTO),
            width=350,
            height=300,
            padding=10
        ),
        actions=[
            salvar_embarcacao,
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
        content=ft.Text("Você realmente deseja excluir esta embarcação?"),
        actions=[
            ft.TextButton("Cancelar", on_click=cancelar_exclusao),
            ft.TextButton("Excluir", on_click=confirmar_exclusao),
        ]
    )
    page.overlay.append(confirm_dialog)

    campo_pesquisa = ft.TextField(
        label="Pesquisar embarcação (por nome ou ID)",
        visible=True,
        on_change=lambda e: filtrar_embarcacoes(e.control.value),
        prefix_icon=ft.Icons.SEARCH,
        width=500
    )

    def filtrar_embarcacoes(query):
        tabela.rows.clear()
        for i, e in enumerate(embarcacoes):
            if (
                query.lower() in e["nome"].lower()
                or query == str(e["id"])
            ):
                tabela.rows.append(criar_linha_tabela(i, e))
        page.update()

    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("NOME")),
            ft.DataColumn(ft.Text("CAPACIDADE")),
            ft.DataColumn(ft.Text("AÇÕES")),
        ],
        rows=[]
    )

    atualizar_lista()

    def abrir_dialogo_cadastro(e):
        embarcacao_em_edicao["index"] = None
        limpar_campos()
        dialog.open = True
        page.update()

    return ft.View(
        route="/embarcacoes",
        appbar=ft.AppBar(
            title=ft.Row([
                ft.Icon(name=ft.Icons.DIRECTIONS_BOAT, color=ft.Colors.WHITE),
                ft.Text("Embarcações", color=ft.Colors.WHITE),
            ], spacing=10),
            leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, tooltip="Voltar", icon_color=ft.Colors.WHITE, on_click=voltar_home),
            bgcolor=ft.Colors.BLUE
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
                            bgcolor=ft.Colors.BLUE,
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