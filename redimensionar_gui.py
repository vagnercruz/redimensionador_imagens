import os
from PIL import Image, ImageOps
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
        if largura <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erro", "Digite uma largura válida.")
        return

    formato = formato_var.get()
    qualidade = qualidade_scale.get()

    arquivos = [
        f for f in os.listdir(pasta_entrada)
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
    ]

    if not arquivos:
        messagebox.showwarning("Aviso", "Nenhuma imagem encontrada.")
        return

    pasta_saida = os.path.join(pasta_entrada, "imagens_redimensionadas")
    os.makedirs(pasta_saida, exist_ok=True)

    progresso["maximum"] = len(arquivos)
    progresso["value"] = 0
    status_label.config(text="Iniciando...")

    for i, arquivo in enumerate(arquivos, start=1):
        caminho = os.path.join(pasta_entrada, arquivo)

        try:
            with Image.open(caminho) as img:
                img = ImageOps.exif_transpose(img)

                w, h = img.size
                proporcao = largura / w
                nova_altura = int(h * proporcao)

                img = img.resize((largura, nova_altura), Image.LANCZOS)

                nome_base = os.path.splitext(arquivo)[0]
                extensao = formato.lower()
                caminho_saida = os.path.join(
                    pasta_saida,
                    f"{nome_base}.{extensao}"
                )

                if formato == "PNG":
                    img.save(caminho_saida, format="PNG")
                else:
                    img = img.convert("RGB")
                    img.save(
                        caminho_saida,
                        format=formato,
                        quality=qualidade
                    )
        except Exception:
            pass

        progresso["value"] = i
        status_label.config(
            text=f"Processando {i} de {len(arquivos)}"
        )
        janela.update_idletasks()

    status_label.config(text="Concluído!")
    messagebox.showinfo(
        "Finalizado",
        f"{len(arquivos)} imagens redimensionadas com sucesso!\n\n"
        f"Salvas em:\n{pasta_saida}"
    )

janela = tk.Tk()
janela.title("Redimensionador de Imagens")
janela.geometry("460x380")
janela.resizable(False, False)

entrada_pasta = tk.StringVar()
formato_var = tk.StringVar(value="JPG")

tk.Label(janela, text="Pasta das imagens:").pack(pady=5)
tk.Entry(janela, textvariable=entrada_pasta, width=52).pack()
tk.Button(
    janela,
    text="Selecionar pasta",
    command=selecionar_pasta
).pack(pady=5)

tk.Label(janela, text="Largura desejada (px):").pack(pady=5)
largura_entry = tk.Entry(janela)
largura_entry.pack()

tk.Label(janela, text="Formato de saída:").pack(pady=5)
ttk.Combobox(
    janela,
    textvariable=formato_var,
    values=["JPG", "PNG", "WEBP"],
    state="readonly",
    width=15
).pack()

tk.Label(janela, text="Qualidade (JPG / WEBP):").pack(pady=5)
qualidade_scale = tk.Scale(
    janela,
    from_=10,
    to=100,
    orient="horizontal",
    length=300
)
qualidade_scale.set(85)
qualidade_scale.pack()

progresso = ttk.Progressbar(janela, length=400)
progresso.pack(pady=15)

status_label = tk.Label(janela, text="Aguardando...")
status_label.pack()

tk.Button(
    janela,
    text="Redimensionar imagens",
    command=redimensionar,
    width=32,
    height=2000,
    bg="#4C53AF",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    activebackground="#4368A0",
    activeforeground="white"
).pack(pady=15)

janela.mainloop()
