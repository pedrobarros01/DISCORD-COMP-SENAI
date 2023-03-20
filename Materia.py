from Prova import Prova

class Materia:
    def __init__(self, nomeMateria: str):
        self.nomeMateria: str = nomeMateria
        self.conteudos: Prova = Prova()
    
    