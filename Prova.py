class Prova:
    def __init__(self,data:str, unidade: str) -> None:
        self.unidade: str = unidade
        self.data: str = data
        self.conteudos: list[str] | list | None = [] | None
    
    def adicionarConteudo(self, conteudo: str):
        self.conteudos.append(conteudo)
        return True
    
    def removerConteudo(self, conteudo: str):
        self.conteudos.remove(conteudo)
        