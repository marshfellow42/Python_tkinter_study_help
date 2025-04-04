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

def update_revert_button():
    """Atualiza a visibilidade do botão de reversão."""
    selected_file = combo.get()
    if not selected_file:
        btn_revert.pack_forget()
        return

    file_path = os.path.join(directory, selected_file + ".json")

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if data["materia_escolhida"]:
        btn_revert.pack(pady=10)
    else:
        btn_revert.pack_forget()

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

    # Atualizar visibilidade do botão de reversão
    update_revert_button()

    # Exibir nova janela com a matéria escolhida
    show_subject_window(chosen_subject)

def revert_subject():
    """Reverte o primeiro item da lista 'materia_escolhida' para 'materia_nao_escolhida'."""
    selected_file = combo.get()
    if not selected_file:
        messagebox.showerror("Erro", "Por favor, selecione um arquivo JSON.")
        return

    file_path = os.path.join(directory, selected_file + ".json")

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not data["materia_escolhida"]:
        messagebox.showinfo("Aviso", "Nenhuma matéria para reverter!")
        return

    # Reverter o primeiro item da lista 'materia_escolhida'
    reverted_subject = data["materia_escolhida"].pop(0)
    data["materia_nao_escolhida"].append(reverted_subject)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    messagebox.showinfo("Reversão", f"'{reverted_subject}' foi movido de volta para 'materia_nao_escolhida'.")

    # Atualizar visibilidade do botão de reversão
    update_revert_button()

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
root.geometry("400x250")

tk.Label(root, text="Selecione um JSON:").pack(pady=5)

json_files = load_json_files()
combo = ttk.Combobox(root, values=json_files)
if json_files:
    combo.set(json_files[0])  # Seleciona o primeiro JSON por padrão
combo.pack(pady=5)
combo.bind("<<ComboboxSelected>>", lambda e: update_revert_button())

btn_choose = tk.Button(root, text="Escolher Matéria do Dia", command=choose_subject)
btn_choose.pack(pady=10)

btn_revert = tk.Button(root, text="Reverter Última Escolha", command=revert_subject)
btn_revert.pack_forget()  # Ocultar inicialmente

# Verificar se o botão de reversão deve ser exibido inicialmente
update_revert_button()

root.mainloop()
