import flet as ft
from models.portos_controller import PortosController  # Importa o controlador de funcionários

db_portos = PortosController()  # Instancia o controlador de funcionários

portos = []

def View(page: ft.Page):
    porto_para_excluir = {"index": None}
    # Alterado para consistência com produtos.py
    porto_em_edicao = {"index": None} 

    id_field = ft.TextField(label="ID", read_only=True, width=120)

    def voltar_home(e):
        page.go("/admin_home")

    def criar_linha_tabela(i, p):
        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(p["id"]))),
                ft.DataCell(ft.Text(p["nome"], max_lines=2, overflow=ft.TextOverflow.ELLIPSIS)),
                ft.DataCell(ft.Text(p["cidade"], max_lines=2, overflow=ft.TextOverflow.ELLIPSIS)),
                ft.DataCell(ft.Text(str(p["estado"]))),
                ft.DataCell(
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            tooltip="Clique aqui para editar porto",
                            icon_color=ft.Colors.BLUE,
                            on_click=lambda e, idx=i: editar_porto(idx)(e)
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            tooltip="Clique aqui para excluir poto",
                            icon_color=ft.Colors.RED,
                            on_click=lambda e, idx=i: editar_porto(idx)(e)
                        ),
                    ], spacing=5)
                ),
            ]
        )

    def atualizar_lista():
        #tabela.rows.clear()
        #for i, p in enumerate(funcionarios):
        #    tabela.rows.append(criar_linha_tabela(i, p))
        tabela.rows.clear()
        portos.clear()
        portos.extend(db_portos.listar_portos())
        for i, p in enumerate(portos):
            tabela.rows.append(criar_linha_tabela(i, p))
        page.update()

    def editar_porto(index):
        def handler(e):
            # Usando o dicionário para estado de edição
            porto_em_edicao["index"] = index
            porto = portos[index]
            id_field.value = porto["id"]
            nome_field.value = porto["nome"]
            cidade_field.value = porto["cidade"]
            estado_field.value = porto["estado"]
            dialog.open = True
            page.update()
        return handler

    def excluir_porto(index):
        def handler(e):
            porto_para_excluir["index"] = index
            confirm_dialog.open = True
            page.update()
        return handler

    def confirmar_exclusao(e):
        index = porto_para_excluir["index"]
        if index is not None:
            funcionario_id = portos[index]["id"]
            if db_portos.excluir_porto(funcionario_id):
                portos.pop(index)
                atualizar_lista()
        confirm_dialog.open = False
        page.update()

    def cancelar_exclusao(e):
        confirm_dialog.open = False
        page.update()


    def limpar_campos():
        id_field.value = ""
        nome_field.value = ""
        cidade_field.value = ""
        estado_field.value = ""
        # Limpar estado de edição
        porto_em_edicao["index"] = None 
        for f in [nome_field]:
            f.error_text = None
            f.border_color = None # Limpar a cor da borda também

    
    def salvar_porto_click(e):
        campos_obrigatorios = [
            (nome_field, "Nome"),
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

        novo_porto = {
            "nome": nome_field.value,
            "cidade": cidade_field.value,
            "estado": estado_field.value,
        }

        # Usa o dicionário para verificar o estado de edição
        if porto_em_edicao["index"] is None:
            porto_id = db_portos.cadastrar_porto(novo_porto)
            if porto_id:
                novo_porto["id"] = porto_id
                portos.append(novo_porto)
        else:
            #funcionarios[funcionario_em_edicao["index"]] = novo_funcionario
            index = porto_em_edicao["index"]
            porto_id = portos[index]["id"]
            if db_portos.atualizar_porto(porto_id, novo_porto):
                novo_porto["id"] = porto_id
                portos[porto_em_edicao["index"]] = novo_porto

        # Limpar estado de edição após salvar
        porto_em_edicao["index"] = None
        atualizar_lista()
        dialog.open = False
        page.update()

    salvar_porto = ft.ElevatedButton(
        "Salvar",
        on_click=salvar_porto_click,
        tooltip="Clique aqui para salvar este porto", # Adicionado tooltip
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.GREEN,
            color=ft.Colors.WHITE,
        )
    )

    # Campos de entrada
    nome_field = ft.TextField(label="* Nome", width=180)
    cidade_field = ft.TextField(label="Cidade")
    estado_field = ft.TextField(label="Estado")


    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Cadastrar/Editar Porto"),
        content=ft.Container(
            content=ft.Column([
                ft.Row([id_field, nome_field], spacing=10), # Agrupando para layout
                cidade_field,
                estado_field
            ], tight=True, scroll=ft.ScrollMode.AUTO),
            width=350,
            height=520,
            padding=10
        ),
        actions=[
            salvar_porto,
            ft.ElevatedButton(
                "Cancelar",
                tooltip="Clique aqui para cancelar o cadastro", # Adicionado tooltip
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
        content=ft.Text("Você realmente deseja excluir este porto?"),
        actions=[
            ft.TextButton("Cancelar", tooltip="Clique aqui para cancelar a exclusão", on_click=cancelar_exclusao), # Adicionado tooltip
            ft.TextButton("Excluir", tooltip="Clique aqui para excluir este porto", on_click=confirmar_exclusao), # Adicionado tooltip
        ]
    )
    page.overlay.append(confirm_dialog)

    campo_pesquisa = ft.TextField(
        label="Pesquisar porto (por nome ou ID)",
        visible=True,
        on_change=lambda e: filtrar_portos(e.control.value),
        prefix_icon=ft.Icons.SEARCH,
        width=500
    )

    def filtrar_portos(query):
        tabela.rows.clear()
        for i, p in enumerate(portos):
            if (
                query.lower() in p["nome"].lower()
                or query == str(p["id"])
            ):
                tabela.rows.append(criar_linha_tabela(i, p))
        page.update()

    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("NOME")), # Alterado para maiúsculas como em produtos
            ft.DataColumn(ft.Text("CIDADE")), # Alterado para maiúsculas como em produtos
            ft.DataColumn(ft.Text("ESTADO")), # Alterado para maiúsculas como em produtos
            ft.DataColumn(ft.Text("AÇÕES")), # Alterado para maiúsculas como em produtos
        ],
        rows=[]
    )

    atualizar_lista()

    # Função separada para abrir o diálogo de cadastro (igual ao produtos.py)
    def abrir_dialogo_cadastro(e):
        porto_em_edicao["index"] = None
        limpar_campos()
        dialog.open = True
        page.update()


    return ft.View(
        route="/portos",
        appbar=ft.AppBar(
            title=ft.Row([
                ft.Icon(name=ft.Icons.PERSON, color=ft.Colors.WHITE),
                ft.Text("Portos", color=ft.Colors.WHITE),
            ], spacing=10),
            leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, tooltip="Clique aqui para voltar", icon_color=ft.Colors.WHITE, on_click=voltar_home),
            bgcolor=ft.Colors.ORANGE
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
                            bgcolor=ft.Colors.ORANGE,
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