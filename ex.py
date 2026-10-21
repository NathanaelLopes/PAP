def mostrar_mensagem():
    """Isso vai mostrar a mensagem"""
    print(f"Estou aprendendo python")

print(f"mostrar_mensagem('pikachu')")


def fazer_tshirt(tamanho="M", mensagem="Eu adoro Python"):
    """Mostra o tamanho da camiseta e a mensagem"""
    print(f"Tamanho da camiseta: {tamanho}")
    print(f"Mensagem na camiseta: {mensagem}")

fazer_tshirt()
fazer_tshirt(tamanho="L", mensagem="Eu adoro Python")
fazer_tshirt(tamanho="S", mensagem="Eu nao adoro Python")

def descrever_cidade(cidade, pais="Portugal"):
    """Mostra a cidade e o pais"""
    print(f"{cidade} fica em {pais}")

def nome_fomatado(nome, apelido):
    """Devolve um nome completo formatado"""
    completo = f"{nome} {apelido}"
    return completo.title()

artista = nome_fomatado("Nathanael", "Lopes")
print(artista)

def nome_fomatado(nome, apelido, meio=""):
    """Devolve um nome completo formatado"""
    if meio:
        completo = f"{nome} {meio} {apelido}"
    else:
        completo = f"{nome} {apelido}"
    return completo.title()

print(nome_fomatado("Nathanael","Lopes"))
print(nome_fomatado("Nathanael", "Lopes", "Oliveira"))

def cidade_pais(cidade, pais):
    """Mostra a cidade e o pais"""
    return f"cidade: {cidade.title()} e Pais: {pais.title()}"

print(cidade_pais("Fortaleza","Brasil"))
print(cidade_pais("Lisboa","Portugal"))
print(cidade_pais("Terceira","Portugal"))

def criar_album(artista, titulo, faixa="None"):
    """Criar um dicionario de um album"""
    album = {"artista": artista, "titulo": titulo}
    if faixa:
        album["faixa"] = faixa
    return album

print(criar_album("Pink Floyd", "The Wall"))
print(criar_album("Pink Floyd", "The Wall", faixa=26))

def saudar_utlizadores(nomes):
    """Sauda os utilizadores"""
    for nome in nomes:
        msg = f"Olá, {nome.title()}!"
        print(msg)

utlizadores = ["nathanael", "joao", "maria"]
saudar_utlizadores(utlizadores)