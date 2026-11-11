import json

nome = "dados.json"
try:
    with open("dados.json") as f:
        dados = json.load(f)
except FileNotFoundError:
    print("Erro")
