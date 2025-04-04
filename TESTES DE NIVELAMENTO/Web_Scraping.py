import requests
from bs4 import BeautifulSoup
import os
import zipfile

# URL da página da ANS
url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

# Pasta onde os PDFs serão salvos
output_folder = "pdfs"
os.makedirs(output_folder, exist_ok=True)

# Função para baixar arquivos PDF
def baixar_pdf(url, pasta):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        filename = os.path.join(pasta, url.split("/")[-1])
        with open(filename, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Baixado: {filename}")
        return filename
    else:
        print(f"Erro ao baixar {url}")
        return None

# Fazendo a requisição para a página
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Encontrando os links dos PDFs
pdf_links = [a["href"] for a in soup.find_all("a", href=True) if a["href"].endswith(".pdf")]

# Baixando os PDFs
pdf_files = [baixar_pdf(link, output_folder) for link in pdf_links if "Anexo" in link]

# Compactando os PDFs em um único arquivo ZIP
zip_filename = "Anexos_ANS.zip"
with zipfile.ZipFile(zip_filename, "w") as zipf:
    for pdf in pdf_files:
        if pdf:
            zipf.write(pdf, os.path.basename(pdf))

print(f"Arquivos compactados em: {zip_filename}")
