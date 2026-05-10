"""
Calendário Inteligente - Minimize Lateness (Greedy)
Ponto de entrada principal do programa.
"""

import curses
from ui import CalendarioUI

def main():
    try:
        ui = CalendarioUI()
        curses.wrapper(ui.run)
    except KeyboardInterrupt:
        print("\nPrograma encerrado.")

if __name__ == "__main__":
    main()
