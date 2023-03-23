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
    @classmethod
    def printarMaterias(cls, materias: list[Self]):
        msg = ''
        for mat in materias:
            msg += ('**====================================================**\n')
            msg += (f"**{mat.nomeMateria}**\n")
            for prova in mat.provas:
                msg += prova.printarProva()
            msg += ('**====================================================**\n')
        return msg

    def __procurarProva(self, nomeProva: str):
        for provinha in self.provas:
            if provinha.nomeProva.lower() == nomeProva.lower():
                return provinha
        return None

    def adicionarProva(self, unidade: int, data: str, nomeProva: str, notaProva: float):
        if unidade < 1 or unidade > 3:
            return (False, "Unidade fora do range")
        tem = self.__procurarProva(nomeProva)
        if tem:
            return (False, "Já existe essa prova")
        if notaProva < 0 or notaProva > 10:
            return (False, "Nota precisa estar entre 0 e 10")
        prova = Prova(unidade, data, nomeProva, notaProva)
        self.provas.append(prova)
        return (True, "Adicionado com sucesso")

    def adicionarConteudoNumaProva(self, conteudo: str,  nomeProva: str):
        if conteudo.find(',') == -1:
            return (False, "Formatação de conteudos esta errada, Precisa separar por (,)")
        prova = self.__procurarProva(nomeProva)
        if not prova:
            return (False, "Prova não existe no armazenamento do sistema")

        prova.adicionarConteudo(conteudo)
        return True

    
        
    
    
    
    