class restaurante:

    def __init__(self, nome, tipo_cozinha):
        self.nome = nome
        self.tipo_cozinha = tipo_cozinha
        self.servidos = 0

    def descrever(self):
        print(f"Esse e o nome {self.nome}")
        print(f"Esse sao os tipos {self.tipo_cozinha}")

    def abrir(self):
        print(f"O restaurante esta aberto {self.nome}")

    def definir_servidos(self, servidos):
        if servidos >= 0:
            self.servidos
        else:
            print("Não ha servidos")

    def somar_servidos(self, servidos):
        self.servidos += servidos


rest1 = restaurante("Mar doce", "peixe doce")
print(rest1.descrever())
rest1.servidos
rest1.definir_servidos(10)
rest1.somar_servidos(20)

class Carro:
    """represntar um carro."""

    def __init__(self, marca, modelo, ano):
        self.marca = marca
        self.modelo = modelo
        self.ano = ano
        self.km = 0

    def nome_descritivo(self):
        nome = f"{self.ano} {self.marca} {self.modelo}"
        return nome.title()

    def ler_km(self):
        print(f"Esse carro tem {self.km} km.")

meu_carro = Carro('renault', 'clio', 2024)
print(meu_carro.nome_descritivo())
meu_carro.ler_km()
