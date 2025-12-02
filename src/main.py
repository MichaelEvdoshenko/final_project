import tkinter as tk
from ui.gui import StartScreen

def main():
    print("Запуск игры Крестики-нолики...")
    root = tk.Tk()
    app = StartScreen(root)
    root.mainloop()
    print("Игра завершена")

if __name__ == "__main__":
    main()