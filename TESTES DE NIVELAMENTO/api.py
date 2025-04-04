from fastapi import FastAPI, Query
import pandas as pd

app = FastAPI()

df = pd.read_csv("operadoras_ativas.csv")

@app.get("/buscar")
def buscar_operadora(termo: str = Query(..., description="Nome da operadora")):
    resultado = df[df["nome_fantasia"].str.contains(termo, case=False, na=False)]
    return resultado.to_dict(orient="records")

