from datetime import date
 
def hoje_dia0() -> date:
    return date.today()
 
 
def dias_ate(data_alvo: date) -> int:
    return (data_alvo - hoje_dia0()).days
 
 
def minimize_lateness(tarefas: list[dict]) -> dict:
    raise NotImplementedError("faça o algoritmo aqui")
 
 
def validar_tarefa(nome: str, duracao: int, deadline: int) -> list[str]:
    erros = []
    if not nome.strip():
        erros.append("Nome não pode ser vazio.")
    if duracao <= 0:
        erros.append("Duração deve ser maior que zero.")
    if deadline < 0:
        erros.append("Prazo não pode ser negativo (anterior a hoje).")
    return erros
 