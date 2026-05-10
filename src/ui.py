import curses
from datetime import date, timedelta
from scheduler import validar_tarefa, minimize_lateness, hoje_dia0

C_NORMAL   = 0
C_TITLE    = 1
C_SELECTED = 2
C_SUCCESS  = 3
C_WARNING  = 4
C_ERROR    = 5
C_BORDER   = 6
C_DIM      = 7
C_HEADER   = 8


def init_cores():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(C_TITLE,    curses.COLOR_CYAN,   -1)
    curses.init_pair(C_SELECTED, curses.COLOR_BLACK,  curses.COLOR_CYAN)
    curses.init_pair(C_SUCCESS,  curses.COLOR_GREEN,  -1)
    curses.init_pair(C_WARNING,  curses.COLOR_YELLOW, -1)
    curses.init_pair(C_ERROR,    curses.COLOR_RED,    -1)
    curses.init_pair(C_BORDER,   curses.COLOR_BLUE,   -1)
    curses.init_pair(C_DIM,      curses.COLOR_WHITE,  -1)
    curses.init_pair(C_HEADER,   curses.COLOR_BLACK,  curses.COLOR_BLUE)


def safe_addstr(win, y, x, texto, attr=0):
    max_y, max_x = win.getmaxyx()
    if y < 0 or y >= max_y or x < 0:
        return
    espaco = max_x - x - 1
    if espaco <= 0:
        return
    try:
        win.addstr(y, x, texto[:espaco], attr)
    except curses.error:
        pass


# ── Desenho de cabeçalho e rodapé ─────────────────────────────────────────

def desenhar_topo(stdscr):
    max_y, max_x = stdscr.getmaxyx()
    titulo = "  Calendário Inteligente"
    safe_addstr(stdscr, 0, 0, titulo.ljust(max_x - 1),
                curses.color_pair(C_HEADER) | curses.A_BOLD)
    hoje = hoje_dia0().strftime("%d/%m/%Y")
    safe_addstr(stdscr, 1, 2, f"{hoje}",
                curses.color_pair(C_DIM))


def desenhar_linha_h(stdscr, y, char="-"):
    max_y, max_x = stdscr.getmaxyx()
    safe_addstr(stdscr, y, 0, char * (max_x - 1), curses.color_pair(C_BORDER))


def desenhar_rodape(stdscr, texto):
    max_y, max_x = stdscr.getmaxyx()
    safe_addstr(stdscr, max_y - 1, 0, texto[:max_x - 1],
                curses.color_pair(C_DIM) | curses.A_DIM)


# ── Input de linha (curses echo simples) ──────────────────────────────────

def input_linha(stdscr, y, x, prompt, cor_prompt=C_TITLE):
    """Exibe prompt e lê uma linha de texto. Retorna string digitada."""
    safe_addstr(stdscr, y, x, prompt, curses.color_pair(cor_prompt) | curses.A_BOLD)
    stdscr.refresh()
    curses.echo()
    curses.curs_set(1)
    max_y, max_x = stdscr.getmaxyx()
    campo_x = x + len(prompt)
    # limita para não sair da tela
    n = max(1, max_x - campo_x - 1)
    try:
        raw = stdscr.getstr(y, campo_x, n)
        resultado = raw.decode("utf-8", errors="replace").strip()
    except Exception:
        resultado = ""
    curses.noecho()
    curses.curs_set(0)
    return resultado


# ── Telas ──────────────────────────────────────────────────────────────────

def tela_menu(stdscr, n_tarefas):
    """Desenha o menu principal e retorna a tecla pressionada."""
    stdscr.erase()
    max_y, max_x = stdscr.getmaxyx()
    desenhar_topo(stdscr)
    desenhar_linha_h(stdscr, 2)

    opcoes = [
        ("1", "Adicionar Tarefa"),
        ("2", f"Listar Tarefas  ({n_tarefas} cadastrada(s))"),
        ("3", "Escalonar tarefas (minimize lateness)"),
        ("4", "Limpar todas as tarefas"),
        ("0", "Sair"),
    ]

    safe_addstr(stdscr, 3, 2, "MENU PRINCIPAL",
                curses.color_pair(C_TITLE) | curses.A_BOLD)

    for i, (num, desc) in enumerate(opcoes):
        linha = 5 + i
        safe_addstr(stdscr, linha, 4, f"[{num}]", curses.color_pair(C_SELECTED) | curses.A_BOLD)
        safe_addstr(stdscr, linha, 9, desc, curses.color_pair(C_DIM))

    desenhar_linha_h(stdscr, 5 + len(opcoes) + 1)
    escolha = input_linha(stdscr, 5 + len(opcoes) + 2, 2, "Opção: ", C_TITLE)
    return escolha.strip()


def tela_adicionar_tarefa(stdscr, tarefas):
    stdscr.erase()
    max_y, max_x = stdscr.getmaxyx()
    desenhar_topo(stdscr)
    desenhar_linha_h(stdscr, 2)

    safe_addstr(stdscr, 3, 2, "ADICIONAR TAREFA",
                curses.color_pair(C_TITLE) | curses.A_BOLD)
    safe_addstr(stdscr, 4, 2,
                "Preencha os campos abaixo. ESC ou vazio = cancelar.",
                curses.color_pair(C_DIM))
    desenhar_linha_h(stdscr, 5)

    hoje = hoje_dia0()

    # Nome
    nome = input_linha(stdscr, 7, 2, "Nome da Tarefa  : ")
    if not nome:
        return False

    # Duração
    dur_str = input_linha(stdscr, 9, 2, "Duração (em dias)  : ")
    if not dur_str:
        return False
    try:
        duracao = int(dur_str)
    except ValueError:
        stdscr.erase()
        desenhar_topo(stdscr)
        safe_addstr(stdscr, 4, 2, "ERRO: Duração deve ser um numero inteiro.",
                    curses.color_pair(C_ERROR) | curses.A_BOLD)
        safe_addstr(stdscr, 6, 2, "Pressione qualquer tecla para voltar.",
                    curses.color_pair(C_DIM))
        stdscr.refresh()
        stdscr.getch()
        return False

    # Prazo
    safe_addstr(stdscr, 11, 2,
                "Prazo: data DD/MM/AAAA ou número de dias a partir de hoje",
                curses.color_pair(C_DIM))
    prazo_str = input_linha(stdscr, 12, 2, "Prazo final: ")
    if not prazo_str:
        return False

    try:
        if "/" in prazo_str:
            d, m, a = prazo_str.split("/")
            data_prazo = date(int(a), int(m), int(d))
            deadline = (data_prazo - hoje).days
        else:
            deadline = int(prazo_str)
            data_prazo = hoje + timedelta(days=deadline)
    except (ValueError, TypeError):
        stdscr.erase()
        desenhar_topo(stdscr)
        safe_addstr(stdscr, 4, 2, "ERRO: Formato de prazo inválido.",
                    curses.color_pair(C_ERROR) | curses.A_BOLD)
        safe_addstr(stdscr, 5, 2, "Use DD/MM/AAAA ou um número de dias.",
                    curses.color_pair(C_DIM))
        safe_addstr(stdscr, 7, 2, "Pressione qualquer tecla para voltar.",
                    curses.color_pair(C_DIM))
        stdscr.refresh()
        stdscr.getch()
        return False

    erros = validar_tarefa(nome, duracao, deadline)
    if erros:
        stdscr.erase()
        desenhar_topo(stdscr)
        safe_addstr(stdscr, 4, 2, "ERRO: Dados inválidos:",
                    curses.color_pair(C_ERROR) | curses.A_BOLD)
        for i, e in enumerate(erros):
            safe_addstr(stdscr, 6 + i, 4, "- " + e, curses.color_pair(C_WARNING))
        safe_addstr(stdscr, 8 + len(erros), 2, "Pressione qualquer tecla para voltar.",
                    curses.color_pair(C_DIM))
        stdscr.refresh()
        stdscr.getch()
        return False

    tarefas.append({
        "id":       len(tarefas) + 1,
        "nome":     nome,
        "duracao":  duracao,
        "deadline": deadline,
        "_data":    data_prazo,
    })

    # Confirmação
    stdscr.erase()
    desenhar_topo(stdscr)
    desenhar_linha_h(stdscr, 2)
    safe_addstr(stdscr, 4, 2, "Tarefa adicionada com sucesso!",
                curses.color_pair(C_SUCCESS) | curses.A_BOLD)
    safe_addstr(stdscr, 6, 4, f"Nome   : {nome}", curses.color_pair(C_DIM))
    safe_addstr(stdscr, 7, 4, f"Duracao: {duracao} dia(s)", curses.color_pair(C_DIM))
    safe_addstr(stdscr, 8, 4,
                f"Prazo  : dia {deadline} ({data_prazo.strftime('%d/%m/%Y')})",
                curses.color_pair(C_DIM))
    safe_addstr(stdscr, 10, 2, "Pressione qualquer tecla para voltar.",
                curses.color_pair(C_DIM))
    stdscr.refresh()
    stdscr.getch()
    return True


def tela_listar_tarefas(stdscr, tarefas):
    stdscr.erase()
    max_y, max_x = stdscr.getmaxyx()
    desenhar_topo(stdscr)
    desenhar_linha_h(stdscr, 2)

    safe_addstr(stdscr, 3, 2, f"TAREFAS CADASTRADAS ({len(tarefas)})",
                curses.color_pair(C_TITLE) | curses.A_BOLD)
    desenhar_linha_h(stdscr, 4)

    if not tarefas:
        safe_addstr(stdscr, 6, 4, "Nenhuma tarefa cadastrada ainda.",
                    curses.color_pair(C_WARNING))
    else:
        cab = f"  {'#':>2}  {'Nome':<24}  {'Dur':>5}  {'Prazo':>7}  {'Data':>10}"
        safe_addstr(stdscr, 5, 2, cab, curses.color_pair(C_TITLE) | curses.A_BOLD)
        safe_addstr(stdscr, 6, 2, "-" * min(60, max_x - 4), curses.color_pair(C_BORDER))

        for i, t in enumerate(tarefas):
            linha = 7 + i
            if linha >= max_y - 3:
                safe_addstr(stdscr, linha, 4, "... (mais tarefas acima do limite da tela)",
                            curses.color_pair(C_DIM))
                break
            data_str = t.get("_data", date.today()).strftime("%d/%m/%Y")
            texto = (f"  {t['id']:>2}  {t['nome']:<24.24}  "
                     f"{t['duracao']:>4}d  {t['deadline']:>6}d  {data_str:>10}")
            cor = C_SUCCESS if i % 2 == 0 else C_DIM
            safe_addstr(stdscr, linha, 2, texto, curses.color_pair(cor))

    linha_rodape = max(10, 7 + len(tarefas) + 1)
    desenhar_linha_h(stdscr, min(linha_rodape, max_y - 3))
    safe_addstr(stdscr, min(linha_rodape + 1, max_y - 2), 2,
                "Pressione qualquer tecla para voltar.",
                curses.color_pair(C_DIM))
    stdscr.refresh()
    stdscr.getch()


def tela_resultado(stdscr, tarefas):
    if not tarefas:
        stdscr.erase()
        desenhar_topo(stdscr)
        safe_addstr(stdscr, 4, 2, "Nenhuma tarefa para escalonar.",
                    curses.color_pair(C_WARNING) | curses.A_BOLD)
        safe_addstr(stdscr, 6, 2, "Pressione qualquer tecla para voltar.",
                    curses.color_pair(C_DIM))
        stdscr.refresh()
        stdscr.getch()
        return

    try:
        resultado = minimize_lateness(tarefas)
    except NotImplementedError:
        stdscr.erase()
        desenhar_topo(stdscr)
        safe_addstr(stdscr, 4, 2, "scheduler.py ainda nao foi implementado.",
                    curses.color_pair(C_WARNING) | curses.A_BOLD)
        safe_addstr(stdscr, 5, 2, "Complete a funcao minimize_lateness() la.",
                    curses.color_pair(C_DIM))
        safe_addstr(stdscr, 7, 2, "Pressione qualquer tecla para voltar.",
                    curses.color_pair(C_DIM))
        stdscr.refresh()
        stdscr.getch()
        return
    except Exception as e:
        stdscr.erase()
        desenhar_topo(stdscr)
        safe_addstr(stdscr, 4, 2, "Erro no scheduler:", curses.color_pair(C_ERROR) | curses.A_BOLD)
        safe_addstr(stdscr, 5, 4, str(e)[:70], curses.color_pair(C_DIM))
        safe_addstr(stdscr, 7, 2, "Pressione qualquer tecla para voltar.",
                    curses.color_pair(C_DIM))
        stdscr.refresh()
        stdscr.getch()
        return

    stdscr.erase()
    max_y, max_x = stdscr.getmaxyx()
    desenhar_topo(stdscr)
    desenhar_linha_h(stdscr, 2)

    viavel       = resultado["viavel"]
    max_lateness = resultado["max_lateness"]
    detalhes     = resultado["detalhes"]

    if viavel:
        safe_addstr(stdscr, 3, 2, "RESULTADO: Todas as tarefas no prazo!",
                    curses.color_pair(C_SUCCESS) | curses.A_BOLD)
    else:
        safe_addstr(stdscr, 3, 2, f"RESULTADO: Atraso maximo = {max_lateness} dia(s)",
                    curses.color_pair(C_ERROR) | curses.A_BOLD)

    desenhar_linha_h(stdscr, 4)

    cab = f"  {'#':>2}  {'Nome':<20}  {'Ini':>4}  {'Fim':>4}  {'Prazo':>5}  {'Lateness':>8}"
    safe_addstr(stdscr, 5, 2, cab, curses.color_pair(C_TITLE) | curses.A_BOLD)
    safe_addstr(stdscr, 6, 2, "-" * min(62, max_x - 4), curses.color_pair(C_BORDER))

    for i, det in enumerate(detalhes):
        linha = 7 + i
        if linha >= max_y - 3:
            safe_addstr(stdscr, linha, 4, "... (mais tarefas acima do limite da tela)",
                        curses.color_pair(C_DIM))
            break
        t  = det["tarefa"]
        lt = det["lateness"]
        cor = C_ERROR if lt > 0 else C_SUCCESS
        texto = (f"  {t['id']:>2}  {t['nome']:<20.20}  "
                 f"{det['inicio']:>4}  {det['fim']:>4}  "
                 f"{t['deadline']:>5}  {lt:>+8}")
        safe_addstr(stdscr, linha, 2, texto, curses.color_pair(cor))

    linha_rodape = min(7 + len(detalhes) + 1, max_y - 3)
    desenhar_linha_h(stdscr, linha_rodape)
    safe_addstr(stdscr, linha_rodape + 1, 2,
                "Pressione qualquer tecla para voltar.", curses.color_pair(C_DIM))
    stdscr.refresh()
    stdscr.getch()


def tela_limpar(stdscr, tarefas):
    stdscr.erase()
    desenhar_topo(stdscr)
    desenhar_linha_h(stdscr, 2)
    safe_addstr(stdscr, 4, 2, "Tem certeza que deseja remover TODAS as tarefas?",
                curses.color_pair(C_WARNING) | curses.A_BOLD)
    confirma = input_linha(stdscr, 6, 2, "Digite S para confirmar: ")
    if confirma.upper() == "S":
        tarefas.clear()
        safe_addstr(stdscr, 8, 2, "Todas as tarefas foram removidas.",
                    curses.color_pair(C_SUCCESS) | curses.A_BOLD)
    else:
        safe_addstr(stdscr, 8, 2, "Operacao cancelada.",
                    curses.color_pair(C_DIM))
    safe_addstr(stdscr, 10, 2, "Pressione qualquer tecla para voltar.",
                curses.color_pair(C_DIM))
    stdscr.refresh()
    stdscr.getch()


# ── Classe principal ───────────────────────────────────────────────────────

class CalendarioUI:
    def __init__(self):
        self.tarefas = []

    def run(self, stdscr):
        curses.curs_set(0)
        stdscr.keypad(True)
        init_cores()

        while True:
            escolha = tela_menu(stdscr, len(self.tarefas))
            if escolha == "1":
                tela_adicionar_tarefa(stdscr, self.tarefas)
            elif escolha == "2":
                tela_listar_tarefas(stdscr, self.tarefas)
            elif escolha == "3":
                tela_resultado(stdscr, self.tarefas)
            elif escolha == "4":
                tela_limpar(stdscr, self.tarefas)
            elif escolha == "0":
                break