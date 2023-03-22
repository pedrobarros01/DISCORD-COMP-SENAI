class Prova:
    def __init__(self, unidade: str, data: str, nomeProva: str) -> None:
        self.unidade: str = unidade
        self.data: str = data
        self.nomeProva: str = nomeProva
        self.conteudos: list[str] = []
    
    def adicionarConteudo(self, conteudo: str):
        conteudoSplitado = conteudo.split(',')
        conteudoSplitado.remove('')
        self.conteudos.extend(conteudoSplitado)
    
    def removerConteudo(self, conteudo: str):
        self.conteudos.remove(conteudo)
    
    def printarProva(self):
        pass
        