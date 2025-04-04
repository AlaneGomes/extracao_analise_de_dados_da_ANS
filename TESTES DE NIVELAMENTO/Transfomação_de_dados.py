import pdfplumber
import pandas as pd
import zipfile
import os
pdf_file = "pdfs/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
csv_filename = "Rol_de_Procedimentos.csv"
data = []
with pdfplumber.open(pdf_file) as pdf:
    for page in pdf.pages:
        tables = page.extract_table()
        if tables:
            for row in tables:
                data.append(row)
df = pd.DataFrame(data)
df.columns = df.iloc[0]  
df = df[1:] 
df.replace({"OD": "Odontológico", "AMB": "Ambulatorial"}, inplace=True)
df.to_csv(csv_filename, index=False, encoding="utf-8")
zip_filename = "Teste_AlaneGomes.zip"
with zipfile.ZipFile(zip_filename, "w") as zipf:
    zipf.write(csv_filename, os.path.basename(csv_filename))

print(f"Arquivo CSV gerado e compactado como: {zip_filename}")
