import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def selecionar_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        entrada_pasta.set(pasta)

def redimensionar():
    pasta_entrada = entrada_pasta.get()

    if not pasta_entrada:
        messagebox.showerror("Erro", "Selecione uma pasta com imagens.")
        return

    try:
        largura = int(largura_entry.get())
    except ValueError:
        messagebox.showerror("Erro", "Digite uma largura válida.")
        return

    arquivos = [
        f for f in os.listdir(pasta_entrada)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    if not arquivos:
        messagebox.showwarning("Aviso", "Nenhuma imagem encontrada.")
        return

    pasta_saida = os.path.join(pasta_entrada, "imagens_redimensionadas")
    os.makedirs(pasta_saida, exist_ok=True)

    progresso["maximum"] = len(arquivos)
    progresso["value"] = 0

    for i, arquivo in enumerate(arquivos, start=1):
        caminho = os.path.join(pasta_entrada, arquivo)

        try:
            with Image.open(caminho) as img:
                w, h = img.size
                proporcao = largura / w
                nova_altura = int(h * proporcao)

                img.resize(
                    (largura, nova_altura),
                    Image.LANCZOS
                ).save(os.path.join(pasta_saida, arquivo))
        except:
            pass

        progresso["value"] = i
        status_label.config(text=f"Processando {i} de {len(arquivos)}")
        janela.update_idletasks()

    status_label.config(text="Concluído!")
    messagebox.showinfo(
        "Finalizado",
        f"{len(arquivos)} imagens redimensionadas com sucesso!"
    )

janela = tk.Tk()
janela.title("Redimensionador de Imagens")
janela.geometry("420x280")
janela.resizable(False, False)

entrada_pasta = tk.StringVar()

tk.Label(janela, text="Pasta das imagens:").pack(pady=5)
tk.Entry(janela, textvariable=entrada_pasta, width=48).pack()
tk.Button(janela, text="Selecionar pasta", command=selecionar_pasta).pack(pady=5)

tk.Label(janela, text="Largura desejada (px):").pack(pady=5)
largura_entry = tk.Entry(janela)
largura_entry.pack()

progresso = ttk.Progressbar(janela, length=350)
progresso.pack(pady=15)

status_label = tk.Label(janela, text="Aguardando...")
status_label.pack()

tk.Button(
    janela,
    text="Redimensionar imagens",
    command=redimensionar
).pack(pady=10)

janela.mainloop()
