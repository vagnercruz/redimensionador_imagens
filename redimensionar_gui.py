import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox

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

    pasta_saida = os.path.join(pasta_entrada, "imagens_redimensionadas")
    os.makedirs(pasta_saida, exist_ok=True)

    arquivos_processados = 0

    for arquivo in os.listdir(pasta_entrada):
        if arquivo.lower().endswith((".jpg", ".jpeg", ".png")):
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

                arquivos_processados += 1
            except:
                pass

    if arquivos_processados == 0:
        messagebox.showwarning("Aviso", "Nenhuma imagem encontrada.")
    else:
        messagebox.showinfo(
            "Concluído",
            f"{arquivos_processados} imagens redimensionadas!\n\nSalvas em:\n{pasta_saida}"
        )

# ===== INTERFACE =====

janela = tk.Tk()
janela.title("Redimensionador de Imagens")
janela.geometry("400x220")
janela.resizable(False, False)

entrada_pasta = tk.StringVar()

tk.Label(janela, text="Pasta das imagens:").pack(pady=5)
tk.Entry(janela, textvariable=entrada_pasta, width=45).pack()
tk.Button(janela, text="Selecionar pasta", command=selecionar_pasta).pack(pady=5)

tk.Label(janela, text="Largura desejada (px):").pack(pady=5)
largura_entry = tk.Entry(janela)
largura_entry.pack()

tk.Button(janela, text="Redimensionar imagens", command=redimensionar).pack(pady=15)

janela.mainloop()
