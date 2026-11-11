import json

nome = 'numeros.json'
with open(nome) as f:
    numeros = json.load(f)

print(numeros)
print(sum(numeros))
