from datetime import date
 
def hoje_dia0() -> date:
    return date.today()
 
 
def dias_ate(data_alvo: date) -> int:
    return (data_alvo - hoje_dia0()).days
 
 
def minimize_lateness(tarefas: list[dict]) -> dict:
    """
    Escalona as tarefas pelo algoritmo Earliest Deadline First (EDF),
    o qual minimiza o maior atraso entre todas as tarefas.

    Cada tarefa deve possuir, no mínimo:
    - "duracao": tempo necessário para executá-la;
    - "deadline": prazo limite da tarefa.

    Retorna:
    {
        "ordem": [tarefas ordenadas por deadline],
        "detalhes": [
            {
                "tarefa": tarefa,
                "inicio": instante de início,
                "fim": instante de término,
                "lateness": fim - deadline,
            },
            ...
        ],
        "max_lateness": maior valor de lateness encontrado,
        "viavel": True se nenhuma tarefa atrasar, False caso contrário,
    }
    """
    if not tarefas:
        return {
            "ordem": [],
            "detalhes": [],
            "max_lateness": 0,
            "viavel": True,
        }

    # Regra: executar primeiro quem possui o menor deadline.
    # O id serve apenas como desempate para deixar o resultado determinístico.
    tarefas_ordenadas = sorted(
        tarefas,
        key=lambda tarefa: (tarefa["deadline"], tarefa.get("id", 0)),
    )

    tempo_atual = 0
    max_lateness = float("-inf")
    detalhes = []

    for tarefa in tarefas_ordenadas:
        inicio = tempo_atual
        fim = inicio + tarefa["duracao"]
        lateness = fim - tarefa["deadline"]

        detalhes.append({
            "tarefa": tarefa,
            "inicio": inicio,
            "fim": fim,
            "lateness": lateness,
        })

        tempo_atual = fim
        max_lateness = max(max_lateness, lateness)

    return {
        "ordem": tarefas_ordenadas,
        "detalhes": detalhes,
        "max_lateness": max_lateness,
        "viavel": max_lateness <= 0,
    }
 
 
def validar_tarefa(nome: str, duracao: int, deadline: int) -> list[str]:
    erros = []
    if not nome.strip():
        erros.append("Nome não pode ser vazio.")
    if duracao <= 0:
        erros.append("Duração deve ser maior que zero.")
    if deadline < 0:
        erros.append("Prazo não pode ser negativo (anterior a hoje).")
    return erros
 