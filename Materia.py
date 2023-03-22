from Prova import Prova
from typing import Self
'''
Primeiro preciso de uma materia
Dps vou adicionando as provas desta materia
Cada Prova precisa de uma unidade, *conteudos e uma data
'''
class Materia:
    def __init__(self, nomeMateria: str):
        self.nomeMateria: str = nomeMateria
        self.provas: list[Prova] | None = []
    
    @classmethod
    def buscarMateria(cls, materias: list[Self], materia: str) -> Self | None:
        for mat in materias:
            print(mat.nomeMateria)
            if mat.nomeMateria.lower() == materia.lower():
                return mat
        return None

    def __procurarProva(self, nomeProva: str):
        for provinha in self.provas:
            if provinha.nomeProva.lower() == nomeProva.lower():
                return provinha
        return None

    def adicionarProva(self, unidade: int, data: str, nomeProva: str):
        if unidade < 1 or unidade > 3:
            return False
        tem = self.__procurarProva(nomeProva)
        if tem:
            return False
        prova = Prova(unidade, data, nomeProva)
        self.provas.append(prova)
        return True

    def adicionarConteudoNumaProva(self, conteudo: str,  nomeProva: str):
        prova = self.__procurarProva(nomeProva)
        if not prova:
            return False

        prova.adicionarConteudo(conteudo)
        return True

    def printarProva(self):
        
        pass
    
    
    
    