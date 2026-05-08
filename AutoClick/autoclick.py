import tkinter as tk
from tkinter import messagebox
import pyautogui
# PT: Zera o atraso padrão entre comandos | EN: Zeroes the default delay between commands
pyautogui.PAUSE = 0
import keyboard
import time
import threading
import sys

# PT: Classe principal do aplicativo | EN: Main application class
class AutoClickerApp:
    def __init__(self, root):
        # PT: Configurações da janela principal | EN: Main window settings
        self.root = root
        self.root.title("Auto-Clicker")
        self.root.geometry("350x280")
        self.root.resizable(False, False)

        # PT: Variáveis para controle de estado | EN: State control variables
        self.clicando = False
        self.intervalo = 1.0

        # PT: Título de instrução na interface | EN: Instruction title on the interface
        self.label_instrucao = tk.Label(root, text="Defina o intervalo entre os cliques:", font=("Arial", 11, "bold"))
        self.label_instrucao.pack(pady=(15, 10))
        
        # PT: Container para organizar os campos de tempo | EN: Container to organize time fields
        frame_tempos = tk.Frame(root)
        frame_tempos.pack()

        # PT: Campos de entrada: Horas, Minutos, Segundos e Milissegundos
        # EN: Input fields: Hours, Minutes, Seconds, and Milliseconds

        # Horas / Hours
        self.entry_horas = tk.Entry(frame_tempos, width=5, justify="center", font=("Arial", 12))
        self.entry_horas.insert(0, "0")
        self.entry_horas.grid(row=0, column=0, padx=5)
        tk.Label(frame_tempos, text="Horas/Hrs", font=("Arial", 9)).grid(row=1, column=0)

        # Minutos / Minutes
        self.entry_minutos = tk.Entry(frame_tempos, width=5, justify="center", font=("Arial", 12))
        self.entry_minutos.insert(0, "0")
        self.entry_minutos.grid(row=0, column=1, padx=5)
        tk.Label(frame_tempos, text="Mins", font=("Arial", 9)).grid(row=1, column=1)

        # Segundos / Seconds
        self.entry_segundos = tk.Entry(frame_tempos, width=5, justify="center", font=("Arial", 12))
        self.entry_segundos.insert(0, "1")
        self.entry_segundos.grid(row=0, column=2, padx=5)
        tk.Label(frame_tempos, text="Segs", font=("Arial", 9)).grid(row=1, column=2)

        # Milissegundos / Milliseconds
        self.entry_milis = tk.Entry(frame_tempos, width=5, justify="center", font=("Arial", 12))
        self.entry_milis.insert(0, "0")
        self.entry_milis.grid(row=0, column=3, padx=5)
        tk.Label(frame_tempos, text="Milis/Ms", font=("Arial", 9)).grid(row=1, column=3)

        # PT: Informação sobre o atalho de teclado | EN: Information about the keyboard shortcut
        self.label_atalho = tk.Label(root, text="Atalho/Shortcut: F6", font=("Arial", 11, "bold"))
        self.label_atalho.pack(pady=(25, 5))

        # PT: Texto de status (Ligado/Desligado) | EN: Status text (On/Off)
        self.label_status = tk.Label(root, text="Status: DESLIGADO", font=("Arial", 14, "bold"), fg="red")
        self.label_status.pack(pady=5)

        # PT: Registra o atalho global F6 | EN: Registers the global F6 shortcut
        keyboard.add_hotkey('F6', self.alternar_clique)

        # PT: Cria e inicia a thread secundária para os cliques | EN: Creates and starts the secondary thread for clicking
        self.thread_cliques = threading.Thread(target=self.loop_de_cliques)
        self.thread_cliques.daemon = True # PT: Fecha junto com a janela | EN: Closes with the window
        self.thread_cliques.start()

    def alternar_clique(self):
        # PT: Encaminha a chamada para a thread principal | EN: Forwards the call to the main thread
        self.root.after(0, self._executar_alternar)

    def _executar_alternar(self):
        # PT: Lógica para parar o clicker | EN: Logic to stop the clicker
        if self.clicando:
            self.clicando = False
            self.label_status.config(text="Status: DESLIGADO", fg="red")
            return

        # PT: Tenta converter as entradas e validar os valores | EN: Tries to convert inputs and validate values
        try:
            h = int(self.entry_horas.get() or "0")
            m = int(self.entry_minutos.get() or "0")
            s = int(self.entry_segundos.get() or "0")
            ms = int(self.entry_milis.get() or "0")
            
            tempo_total = (h * 3600) + (m * 60) + s + (ms / 1000.0)
            
            # PT: Bloqueia intervalo zero por segurança | EN: Blocks zero interval for safety
            if tempo_total == 0:
                messagebox.showwarning("Segurança/Safety", "O intervalo não pode ser zero | Interval cannot be zero.")
                return

            if tempo_total < 0:
                raise ValueError
                
            self.intervalo = tempo_total
            
        except ValueError:
            # PT: Trata erros de digitação | EN: Handles typing errors
            messagebox.showerror("Erro/Error", "Digite apenas números positivos | Enter positive numbers only.")
            return

        # PT: Ativa os cliques se passar na validação | EN: Activates clicking if validation passes
        self.clicando = True
        self.label_status.config(text="Status: LIGADO", fg="green")

    def loop_de_cliques(self):
        # PT: Loop infinito que roda em segundo plano | EN: Infinite loop running in the background
        while True:
            if self.clicando:
                pyautogui.click() # PT: Executa o clique | EN: Performs the click
                
                # PT: Aguarda o intervalo definido | EN: Waits for the defined interval
                if self.intervalo > 0:
                    time.sleep(self.intervalo)
            else:
                # PT: Pequena pausa para economizar processador | EN: Small pause to save CPU
                time.sleep(0.1)

# PT: Inicialização do programa | EN: Program initialization
if __name__ == "__main__":
    janela = tk.Tk()
    app = AutoClickerApp(janela)
    
    # PT: Garante o fechamento total do processo | EN: Ensures full process termination
    janela.protocol("WM_DELETE_WINDOW", sys.exit)
    
    janela.mainloop()
