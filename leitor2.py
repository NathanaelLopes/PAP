with open("pi_digits.txt") as ficheiro:
   # conteudo = ficheiro.read()
   # print(conteudo.rstrip()) 
    linhas = ficheiro.readlines()

pi_string = ""
for linha in linhas:
    pi_string += linha.strip()

print(pi_string)
print(len(pi_string)) 
