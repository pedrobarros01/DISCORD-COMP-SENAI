import discord
from Materia import Materia
from Prova import Prova
from discord.ext import commands
import json
from dotenv import dotenv_values
config = dotenv_values(".env")
intents = discord.Intents.all()
bot = commands.Bot(">", intents=intents)
lista_materias: list[Materia] = []


@bot.event
async def on_ready():
    print(f'Estou pronto -> {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith('>AddMateria'):
        materia = message.content.split('>AddMateria')[1]
        materia = materia.split(' ')[1]
        materiaObj = Materia(materia)
        lista_materias.append(materiaObj)
        await message.channel.send(f"Materia: {materia} adicionado com sucesso")
    if message.content.startswith('>AddProva'):
        '''
            {
                "materia": "tal",
                "nomeProva": "tal",
                "unidade": 1,2 ou 3,
                "data": "tal",
            }
        '''
        print(lista_materias)
        msg = message.content.split('>AddProva')[1]
        msgDict = json.loads(msg)
        materia = Materia.buscarMateria(lista_materias, msgDict['materia'])
        if not materia:
            await message.channel.send("Materia informada não existe")
            return

        operacaoConcluida = materia.adicionarProva(msgDict['unidade'], msgDict['data'], msgDict['nomeProva'])
        if not operacaoConcluida:
            await message.channel.send("Prova informada já existe")
            return
        await message.channel.send("Prova adicionada com sucesso")

    if message.content.startswith('>AddConteudo'):
        '''
            {
                "materia": "tal",
                "nomeProva": "tal",
                "conteudos": "tal,tal,tal,tal"
            }
        '''
        msg = message.content.split('>AddConteudo')[1]
        msgDict = json.loads(msg)
        materia = Materia.buscarMateria(lista_materias, msgDict['materia'])
        if not materia:
            await message.channel.send("Materia informada não existe")
            return
        operacaoConcluida = materia.adicionarConteudoNumaProva(msgDict['conteudos'], msgDict['nomeProva'])
        if not operacaoConcluida:
            await message.channel.send("Prova informada nao existe existe")
            return
        await message.channel.send("Conteudos Adicionado com sucesso")
    if message.content.startswith('>PrintarProvas'):
        msg = Materia.printarMaterias(lista_materias)
        await message.channel.send(msg)
    '''if message.content.startswith('>miguez'):
        comp = bot.get_guild()
        miguez = comp.get_member()
        await miguez.kick()'''

bot.run(config['TOKEN'])