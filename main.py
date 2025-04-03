import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random

# Diretório onde os arquivos JSON estão armazenados
directory = "JSON"

def load_json_files():
    """Carrega a lista de arquivos JSON disponíveis no diretório sem a extensão .json."""
    return [f[:-5] for f in os.listdir(directory) if f.endswith(".json")]

def choose_subject():
    """Escolhe uma matéria aleatória e move para 'materia_escolhida'."""
    selected_file = combo.get()
    if not selected_file:
        messagebox.showerror("Erro", "Por favor, selecione um arquivo JSON.")
        return

    file_path = os.path.join(directory, selected_file + ".json")

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not data["materia_nao_escolhida"]:
        messagebox.showinfo("Aviso", "Todas as matérias já foram escolhidas!")
        return

    # Escolher uma matéria aleatória
    chosen_subject = random.choice(data["materia_nao_escolhida"])

    # Atualizar os dados
    data["materia_nao_escolhida"].remove(chosen_subject)
    data["materia_escolhida"].append(chosen_subject)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    # Exibir nova janela com a matéria escolhida
    show_subject_window(chosen_subject)

def show_subject_window(subject):
    """Exibe uma nova janela com a matéria escolhida."""
    new_window = tk.Toplevel(root)
    new_window.title("Matéria do Dia")
    new_window.geometry("300x150")

    label = tk.Label(new_window, text=subject, font=("Arial", 18, "bold"))
    label.pack(expand=True)

# Criando a interface gráfica
root = tk.Tk()
root.title("Escolha de Matéria")
root.geometry("400x200")

tk.Label(root, text="Selecione um JSON:").pack(pady=5)

json_files = load_json_files()
combo = ttk.Combobox(root, values=json_files)
if json_files:
    combo.set(json_files[0])  # Seleciona o primeiro JSON por padrão
combo.pack(pady=5)

btn_choose = tk.Button(root, text="Escolher Matéria do Dia", command=choose_subject)
btn_choose.pack(pady=20)

root.mainloop()
