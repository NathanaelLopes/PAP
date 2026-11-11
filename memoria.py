import json

nome_ficheiro = 'utilizador.json'
try:
    with open(nome_ficheiro) as f:
        utilizador = json.load(f)
except FileNotFoundError:
    utilizador = input("Como te chamas? ")
    with open(nome_ficheiro, 'w') as f:
        json.dump(utilizador, f)
    print(f"Vou lembrar-me de ti, {utilizador}!")
else:
    print(f"Bem-vindo de volta, {utilizador}!")
