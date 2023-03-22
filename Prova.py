class Prova:
    def __init__(self, unidade: str, data: str, nomeProva: str) -> None:
        self.unidade: str = unidade
        self.data: str = data
        self.nomeProva: str = nomeProva
        self.conteudos: list[str] = []
    
    def adicionarConteudo(self, conteudo: str):
        conteudoSplitado = conteudo.split(',')
        
        self.conteudos.extend(conteudoSplitado)
    
    def removerConteudo(self, conteudo: str):
        self.conteudos.remove(conteudo)
    
    def printarProva(self):
        msg = ''
        msg += ('—————————————————\n')
        msg += (f'Unidade {self.unidade}\n')
        msg += (f'NomeProva: {self.nomeProva}\n')
        msg += (f'**Data**: {self.data}\n')
        for conteudo in self.conteudos:
            msg += (f'\t**->{conteudo}**\n')
        return msg

        