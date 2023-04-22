class Prova:
    def __init__(self, unidade: str, data: str, nomeProva: str, notaProva: float) -> None:
        self.unidade: str = unidade
        self.data: str = data
        self.nomeProva: str = nomeProva
        self.notaProva: float = notaProva
        self.conteudos: list[str] = []
    
    def adicionarConteudo(self, conteudo: str):
        conteudoSplitado = conteudo.split(',')
        conteudoSplitado = filter(lambda x: x != '' and x != " ", conteudoSplitado)
        self.conteudos.extend(conteudoSplitado)
    
    def removerConteudo(self, conteudo: str):
        self.conteudos.remove(conteudo)
    
    def adicionarUnicoConteudo(self, conteudo: str):
        self.conteudos.append(conteudo)

    def setConteudos(self, conteudos: list[str]):
        self.conteudos = conteudos
    
    def printarProva(self):
        msg = ''
        msg += ('—————————————————\n')
        msg += (f'Unidade {self.unidade}\n')
        msg += (f'NomeProva: {self.nomeProva}\n')
        msg += (f'Notaprova: {self.notaProva}\n')
        msg += (f'**Data**: {self.data}\n')
        msg += (f'**Conteudos:**\n')
        for conteudo in self.conteudos:
            msg += (f'\t**->{conteudo}**\n')
        return msg
    
    def to_dict(self):
        return {'unidade': self.unidade, 'data': self.data, 'nomeProva': self.nomeProva, 'notaProva': self.notaProva, 'conteudos': [conteudo for conteudo in self.conteudos]}

        