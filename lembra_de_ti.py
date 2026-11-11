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


def obter_utilizador():
    """Devolve o nome guardado, ou None."""
    try:
        with open('utilizador.json') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def novo_utilizador():
    """Pede e guarda um nome novo."""
    nome = input("Como te chamas? ")
    with open('utilizador.json', 'w') as f:
        json.dump(nome, f)
    return nome

def saudar():
    nome = obter_utilizador()
    if nome:
        print(f"Olá de novo, {nome}!")
    else:
        nome = novo_utilizador()
        print(f"Vou lembrar-me, {nome}!")

saudar()
