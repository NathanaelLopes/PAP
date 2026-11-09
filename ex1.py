from random import randint, choice

class Dado:
    def __init__(self, lados=6):
        self.lados = lados

def lancar(self):
    return randint(1, self.lados)

dado = Dado()

for lado in range(1, 11):
    print(f"O lançamento resultou em: {dado.lancar()}/n")