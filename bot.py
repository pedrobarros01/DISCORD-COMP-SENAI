import asyncio
import discord
from Materia import Materia
from discord.ext import commands
import json
from dotenv import dotenv_values
config = dotenv_values(".env")
intents = discord.Intents.all()
bot = commands.Bot(">", intents=intents)
lista_materias: list[Materia] = []

def removerMateria():
    
    pass

def emoji_to_boolean(emoji):
    match emoji:
        case '👍':
            return True
        case _:
            return False

def unicode_to_number(texto):
    match texto:
        case "0️⃣":
            return 0
        case "1️⃣":
            return 1
        case "2️⃣":
            return 2
        case "3️⃣":
            return 3
        case "4️⃣":
            return 4
        case "5️⃣":
            return 5
        case "6️⃣":
            return 6
        case "7️⃣":
            return 7
        case "8️⃣":
            return 8
        case "9️⃣":
            return 9
        case "🔟":
            return 10

def perguntaMateria():
    strPerguntas = ''
        
    emojis = ["0️⃣","1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣","8️⃣","9️⃣","🔟"]
    opcoesAtuais = []
        
    for i, mat in enumerate(lista_materias):
        strPerguntas += f'{emojis[i]} - {mat.nomeMateria}\n'
        opcoesAtuais.append(emojis[i])
    return strPerguntas, opcoesAtuais
        
async def perguntarConteudo(message):
    manterPergunta = True
    listaConteudos: list[str] = []
    while manterPergunta:
        resposta = await perguntar(message, "Deseja adicionar um novo conteudo")
        deseja = emoji_to_boolean(resposta)
        if deseja:
            respostaConteudo = await perguntar_texto(message, "Adicione um novo Conteudo entao:")
            listaConteudos.append(respostaConteudo)
        else:
            manterPergunta = False
    
    return listaConteudos



async def perguntar(mensagem, nome, opcoes: tuple[str]=('👍', '👎')):
    message = mensagem
    await message.channel.send(nome)
    msg = await message.channel.fetch_message(message.channel.last_message_id)
    
    for react in opcoes:
        await msg.add_reaction(react)

    def check(reaction, user):
        return user == message.author

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        #await message.channel.send('👎')
        ''''''
    else:
        return str(reaction.emoji)
    
async def perguntar_texto(mensagem, pergunta):
    message = mensagem
    await message.channel.send(pergunta)

    def check(user):
        return user.author.id == message.author.id and user.channel.id == message.channel.id 

    try:
        response = await bot.wait_for("message", check=check)
    except asyncio.TimeoutError:
        #await message.channel.send('👎')
        ''''''
    else:
        return response.content

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
        tem = Materia.buscarMateria(lista_materias, materiaObj.nomeMateria)
        if tem:
            await message.channel.send("Matéria Já existe")
            return
        lista_materias.append(materiaObj)
        await message.channel.send(f"Materia: {materia} adicionado com sucesso")
    if message.content.startswith('>AddProva'):
        
        '''
            {
                "materia": "tal",
                "nomeProva": "tal",
                "unidade": 1,2 ou 3,
                "data": "tal",
                "notaProva": 7.0
            }
        '''
        
        strPerguntas, opcoesAtuais = perguntaMateria()
        resposta = await perguntar(message, strPerguntas, opcoesAtuais)
        materiaAtual = unicode_to_number(resposta)
        print(materiaAtual)
        '''for i, mat in enumerate(lista_materias):
            #strPerguntas += f'{emojis[i]} - {mat.nomeMateria}\n'
            opcoesAtuais.append(emojis[i])'''
        
        materiaObj = lista_materias[int(materiaAtual)]
        nomeProva = ''
        #materia = Materia.buscarMateria(lista_materias, msgDict['materia'])

        unidade = await perguntar(message, "Por favor, indique a unidade:",("1️⃣","2️⃣","3️⃣","4️⃣"))
        if unidade == "1️⃣":
            unidade = 1
        elif unidade == "2️⃣":
            unidade = 2
        elif unidade == "3️⃣":
            unidade = 3
        elif unidade == "4️⃣":
            unidade = 4
            nomeProva = "EDAG"
            
        data = await perguntar_texto(message, "Por favor, indique a data:")
        
        if nomeProva != "EDAG":
            nomeProva = await perguntar_texto(message, "Por favor, indique o nome da Prova:")
        notaProva = await perguntar_texto(message, "Por favor, indique a nota da Prova:")
        
        operacaoConcluida = materiaObj.adicionarProva(int(unidade), data, nomeProva, float(notaProva))
        if not operacaoConcluida[0]:
            await message.channel.send(operacaoConcluida[1])
            return
        await message.channel.send(operacaoConcluida[1])

    if message.content.startswith('>YN'):
        resposta = await perguntar_texto(message, "Pergunta exemplo")
        print(resposta)

    if message.content.startswith('>AddConteudo'):
        '''
            {
                "materia": "tal",
                "nomeProva": "tal",
                "conteudos": "tal,tal,tal,tal"
            }
        '''
        strPerguntas, opcoesAtuais = perguntaMateria()
        resposta = await perguntar(message, strPerguntas, opcoesAtuais)
        materiaAtual = unicode_to_number(resposta)
        materiaObj = lista_materias[int(materiaAtual)]
        nomeProva = await perguntar_texto(message, "Por favor, indique o nome da prova")
        conteudos = await perguntarConteudo(message)
        conteudosFormatado = ','.join(conteudos)
        operacaoConcluida = materiaObj.adicionarConteudoNumaProva(conteudosFormatado, nomeProva)
        if not operacaoConcluida[0]:
            await message.channel.send(operacaoConcluida[1])
            return
        await message.channel.send(operacaoConcluida[1])
    
    if message.content.startswith('>RemoverProva'):
        strPerguntas, opcoesAtuais = perguntaMateria()
        resposta = await perguntar(message, strPerguntas, opcoesAtuais)
        materiaAtual = unicode_to_number(resposta)
        materiaObj = lista_materias[int(materiaAtual)]
        nomeProva = await perguntar_texto(message, "Por favor, indique o nome da prova")
        teste, mensagem = materiaObj.removerProva(nomeProva)
        if not teste:
            await message.channel.send(mensagem)
            return
        await message.channel.send(mensagem)
    
    if message.content.startswith('>RemoverTodasAsProvas'):
        strPerguntas, opcoesAtuais = perguntaMateria()
        resposta = await perguntar(message, strPerguntas, opcoesAtuais)
        materiaAtual = unicode_to_number(resposta)
        materiaObj = lista_materias[int(materiaAtual)]
        req, msg = materiaObj.removerTodasAsProvas()
        if not req:
            await message.channel.send(msg)
            return
        await message.channel.send(msg)

    if message.content.startswith('>Miguez'):
        comp = bot.get_guild(677252577611612170)
        miguez = comp.get_member(204386578414436352)
        await message.channel.send(f'{miguez.mention} podre!')

    if message.content.startswith('>PrintarProvas'):
        msg = Materia.printarMaterias(lista_materias)
        await message.channel.send(msg)
    '''if message.content.startswith('>miguez'):
        comp = bot.get_guild(991739407314984990)
        miguez = comp.get_member(796901549506166864)
        await miguez.kick()'''

bot.run(config['TOKEN'])