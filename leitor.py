with open("pi_digits.txt") as ficheiro:
   # conteudo = ficheiro.read()
   # print(conteudo.rstrip()) 
    linhas = ficheiro.readlines()


print(linhas)
for linha in linhas:
    print(linha.rstrip())