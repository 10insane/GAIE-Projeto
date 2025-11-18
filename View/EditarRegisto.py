import flet as ft
from Models.RegistoModel import buscarRegistoPorId, atualizarRegisto
from Models.ProblematicaSPO import criarProblematica
from Models.AlunosModel import listarAlunos
from Models.TecnicoModel import listarTecnico
from Controller.EstadoProcessoController import Listar as listarEstadosProcesso

def PaginaEditarRegisto(page: ft.Page):
    # ===== CORES =====
    cor_primaria = "#1E40AF"
    cor_fundo = "#F8FAFC"
    cor_card = "#FFFFFF"
    cor_texto = "#0F172A"
    cor_erro = "#DC2626"
    cor_sucesso = "#10B981"
    cor_borda = "#E2E8F0"

    # ===== PEGAR ID DO REGISTO =====
    idRegisto = page.session.get("registo_editar_id")
    if not idRegisto:
        return ft.View(controls=[ft.Text("Erro: Nenhum registo selecionado")])

    # ===== BUSCAR REGISTO =====
    registo = buscarRegistoPorId(idRegisto)
    if not registo:
        return ft.View(controls=[ft.Text("Erro: Registo não encontrado")])

    # ===== CARREGAR LISTAS =====
    alunos = listarAlunos()
    tecnicos = listarTecnico()
    estados = listarEstadosProcesso()

    # ===== CAMPOS =====
    dropdown_aluno = ft.Dropdown(
        label="Aluno",
        options=[ft.dropdown.Option(str(a["nProcessoAluno"]), a["NomeAluno"]) for a in alunos],
        value=str(registo["nProcessoAluno"]),
        border_color=cor_borda,
        focused_border_color=cor_primaria
    )

    dropdown_estado = ft.Dropdown(
        label="Estado do Processo",
        options=[ft.dropdown.Option(str(e["idEstado"]), e["Estado"]) for e in estados],
        value=str(registo["idEstado"]),
        border_color=cor_borda,
        focused_border_color=cor_primaria
    )

    txt_data = ft.TextField(
        label="Data do Registo",
        value=str(registo["DataArquivo"]) if registo["DataArquivo"] else "",
        border_color=cor_borda,
        focused_border_color=cor_primaria
    )

    txt_descricao = ft.TextField(
        label="Observações",
        value=registo["Observacoes"] or "",
        multiline=True,
        max_lines=3,
        border_color=cor_borda,
        focused_border_color=cor_primaria
    )

    txt_problematica = ft.TextField(
        label="Problemática",
        value=registo.get("tipoProblematica", ""),
        multiline=True,
        max_lines=2,
        border_color=cor_borda,
        focused_border_color=cor_primaria
    )

    dropdown_tecnico = ft.Dropdown(
        label="Técnico Responsável",
        options=[ft.dropdown.Option(str(t["nProcTecnico"]), t["NomeTecnico"]) for t in tecnicos],
        value=str(registo["nProcTecnico"]) if registo.get("nProcTecnico") else None,
        border_color=cor_borda,
        focused_border_color=cor_primaria
    )

    mensagem = ft.Text("", size=14)

    # ===== FUNÇÃO ATUALIZAR =====
    def atualizar(e):
        try:
            # Criar/atualizar problemática
            idProblematica = criarProblematica(txt_problematica.value.strip()) if txt_problematica.value else None

            sucesso = atualizarRegisto(
                idRegisto=idRegisto,
                nProcessoAluno=dropdown_aluno.value,
                idEstado=int(dropdown_estado.value),
                DataArquivo=txt_data.value.strip(),
                Observacoes=txt_descricao.value.strip() if txt_descricao.value else None,
                nProcTecnico=dropdown_tecnico.value,
                idProblematica=idProblematica
            )

            if sucesso:
                mensagem.value = "✔ Registo atualizado com sucesso!"
                mensagem.color = cor_sucesso
                page.update()
                # Redireciona após 1s
                import time
                time.sleep(1)
                page.go("/pagina-principal")
            else:
                raise Exception("Erro ao atualizar registo.")

        except Exception as err:
            mensagem.value = f"❌ {err}"
            mensagem.color = cor_erro
            page.update()

    # ===== VIEW =====
    return ft.View(
        route="/EditarRegisto",
        bgcolor=cor_fundo,
        controls=[
            ft.Container(
                width=700,
                bgcolor=cor_card,
                padding=40,
                border_radius=16,
                content=ft.Column(
                    [
                        ft.Text("Editar Registo", size=28, weight=ft.FontWeight.BOLD, color=cor_texto),
                        ft.Divider(height=30),
                        mensagem,
                        dropdown_aluno,
                        dropdown_estado,
                        txt_data,
                        txt_descricao,
                        txt_problematica,
                        dropdown_tecnico,
                        ft.Row([
                            ft.OutlinedButton("Cancelar", on_click=lambda e: page.go("/pagina-principal")),
                            ft.ElevatedButton("Guardar", on_click=atualizar, bgcolor=cor_primaria, color="white")
                        ], alignment=ft.MainAxisAlignment.END)
                    ],
                    spacing=20
                )
            )
        ]
    )
