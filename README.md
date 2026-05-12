# Calendário Inteligente

**Número da Lista**: 2<br>
**Conteúdo da Disciplina**: Algoritmos Ambiciosos<br>

## Alunos
| Matrícula | Aluno |
| -- | -- |
| 23/1011220 | Davi Camilo Menezes |
| 23/1011800 | Rafael Welz Schadt |

## Sobre
O **Calendário Inteligente** é uma aplicação de interface de linha de comando (CLI) focada no agendamento e otimização de tarefas. O objetivo principal do projeto é aplicar os conceitos de **Algoritmos Ambiciosos (Greedy)**, utilizando o problema de Minimização de Atraso Máximo (*Minimize Lateness*). 

O sistema funciona recebendo uma lista de tarefas, cada uma com uma duração e um prazo final (*deadline*). Ao solicitar o escalonamento, o programa aplica a estratégia **Earliest Deadline First (EDF)**, priorizando a execução das tarefas com os prazos mais curtos. O algoritmo garante a ordem ideal de execução para que, caso o atraso seja inevitável, o maior atraso sofrido por qualquer tarefa seja o menor possível.

## Screenshots
A seguir estão imagens do projeto em funcionamento.

- Menu principal (com todas as funcionalidades):

![alt text](docs/assets/imagem1.png)

- Adicionar uma tarefa:

![alt text](docs/assets/imagem2.png)

![alt text](docs/assets/imagem3.png)

- Visualizar tarefas cadastradas:

![alt text](docs/assets/imagem4.png)

![alt text](docs/assets/imagem5.png)
> Caso não haja tarefa cadastrada.

- Agendamento para minimizar o atraso (cálculo do atraso máximo):

![alt text](docs/assets/imagem6.png)
> Situação em que existe atraso.

![alt text](docs/assets/imagem7.png)
> Situação em que não existe atraso.

![alt text](docs/assets/imagem8.png)
> Caso não haja tarefas para escalonar.

- Excluir todas as tarefas

![alt text](docs/assets/imagem9.png)

![alt text](docs/assets/imagem10.png)

## Instalação
**Linguagem**: Python 3.x<br>
**Framework**: Não foi utilizado<br>
**Pré-requisitos:** O projeto utiliza a biblioteca `curses` para a interface gráfica no terminal. Ela já vem instalada por padrão em sistemas **Linux** e **macOS**. Caso você utilize **Windows**, será necessário instalar um pacote adicional via `pip`.

### Como rodar
1. Clone o repositório para a sua máquina:
```bash
git clone https://github.com/projeto-de-algoritmos-2026/Greed_Calendario-Inteligente.git
```

2. Navegue até a pasta do projeto:
```bash
cd Greed_Calendario-Inteligente
```

3. Entre na pasta src:
```bash
cd src
```

4. OPCIONAL - Caso esteja usando Windows, instale a seguinte dependência:
```bash
pip install windows-curses
```

5. Execute da seguinte maneira:
```bash
cd python main.py
```

## Uso
Como mostrado nas screenshots do trabalho, ao iniciar o programa, o usuário terá acesso ao menu principal com as seguintes opções:

1. **Adicionar Tarefa**: cadastra uma nova tarefa informando nome, duração em dias e prazo final;
2. **Listar Tarefas**: exibe todas as tarefas cadastradas;
3. **Escalonar tarefas**: aplica o algoritmo ambicioso e mostra a ordem de execução, o início, o fim, o prazo e o atraso de cada tarefa, indicando ainda o atraso máximo (caso houver);
4. **Limpar todas as tarefas**: remove os dados que foram cadastrados durante a execução;
5. **Sair**: encerra o programa.

O prazo pode ser informado de duas formas:

- por uma data no formato `DD/MM/AAAA`;
- por um número inteiro, representando a quantidade de dias a partir da data atual.

## Vídeo de Apresentação
Link para o vídeo de apresentação e demonstração do trabalho: [Clique aqui](https://youtu.be/IKaOT2aeHak?si=lu841JBCtQGEwUGo)
