import json

numeros = [2, 3, 5, 7, 11, 13]

nome = 'numeros.json'
with open(nome, 'w') as f:
    json.dump(numeros, f)
