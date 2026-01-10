from PIL import Image
import os

PASTA_ENTRADA = "imagens"
PASTA_SAIDA = "imagens_redimensionadas"

os.makedirs(PASTA_ENTRADA, exist_ok=True)
os.makedirs(PASTA_SAIDA, exist_ok=True)

try:
    LARGURA_DESEJADA = int(input("Digite a largura desejada (ex: 800): "))
except ValueError:
    print("Digite um número válido.")
    exit()

arquivos = os.listdir(PASTA_ENTRADA)

if not arquivos:
    print("⚠️ Coloque imagens na pasta 'imagens'")
    exit()

for arquivo in arquivos:
    if arquivo.lower().endswith((".jpg", ".jpeg", ".png")):
        caminho_entrada = os.path.join(PASTA_ENTRADA, arquivo)
        caminho_saida = os.path.join(PASTA_SAIDA, arquivo)

        with Image.open(caminho_entrada) as img:
            largura_original, altura_original = img.size
            proporcao = LARGURA_DESEJADA / largura_original
            nova_altura = int(altura_original * proporcao)

            img.resize(
                (LARGURA_DESEJADA, nova_altura),
                Image.LANCZOS
            ).save(caminho_saida)

        print(f"✔ {arquivo} redimensionada")

print("Todas as imagens prontas!")
