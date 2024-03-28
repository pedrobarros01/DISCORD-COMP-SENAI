import asyncio
import discord
from Materia import Materia
from discord.ext import commands
import json
from datetime import datetime, time
from discord.ext import tasks
from random import randint
from Prova import Prova
from config import config
import requests

intents = discord.Intents.all()
bot = commands.Bot(">", intents=intents)
dic_final = {
    1.7: 10.0,
    1.8: 9.8,
    1.9: 9.7,
    2.0: 9.5,
    2.1: 9.4,
    2.2: 9.2,
    2.3: 9.1,
    2.4: 8.9,
    2.5: 8.8,
    2.6: 8.6,
    2.7: 8.5,
    2.8: 8.3,
    2.9: 8.2,
    3.0: 8.0,
    3.1: 7.9,
    3.2: 7.7,
    3.3: 7.6,
    3.4: 7.4,
    3.5: 7.3,
    3.6:7.1,
    3.7: 7.0,
    3.8:6.8,
    3.9: 6.7,
    4.0: 6.5,
    4.1: 6.4,
    4.2 :6.2, 
    4.3: 6.1,
    4.4: 5.9,
    4.5: 5.8,
    4.6: 5.6,
    4.7: 5.5,
    4.8: 5.3,
    4.9: 5.2,
    5.0:  5.0,
    5.1: 4.9,
    5.2: 4.7,
    5.3: 4.6,
    5.4: 4.4,
    5.5: 4.3,
    5.6: 4.1,
    5.7: 4.0,
    5.8: 3.8,
    5.9: 3.7,
    6.0: 3.5,
    6.1: 3.4,
    6.2: 3.2,
    6.3: 3.1,
    6.4: 2.9,
    6.5: 2.8,
    6.6: 2.6,
    6.7: 2.5,
    6.8: 2.3,
    6.9: 2.2
}

lista_materias: list[Materia] = []
def checarData(data):
    data = data.split('/')
    if len(data) == 2:
        data.append(str(datetime.now().year))
    elif len(data) != 3:
        return False
    
    delta = datetime(day=int(data[0]), month=int(data[1]), year=int(data[2])) - datetime.now()
    return delta.days + 1

def saber_se_data_prova_ja_passou(data):
    data = data.split('/')
    if len(data) == 3:
        return False
    if len(data) == 2:
        data.append(str(datetime.now().year))

    data_de_hoje = datetime.now()
    data_prova = datetime(day=int(data[0]), month=int(data[1]), year=int(data[2]))
    if data_de_hoje > data_prova:
        return True
    else:
        return False

WHEN = time(19, 18, 40)  # 6:00 PM
channel_id = config['aviso'] # CANAL DE AVISO DE PROVAS # bot.run(config['CANAL']) (?) #

def pegarSalas(ra: str):
    print(f'https://senaiweb.fieb.org.br/MinhaAula/api/aulas?ra={ra}')
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Encoding": "*",
    "Connection": "keep-alive"
    }
    req = requests.get(f'https://senaiweb.fieb.org.br/MinhaAula/api/aulas?ra={ra}', headers=headers)
    data = req.json()
    string = ''
    for aula in data:
        string += f"->Aula: {aula['disciplina']}\n->Predio: {aula['predio']}\n->Andar: {aula['bloco']}\n->Sala: {aula['sala']}\n---------------------\n"
    return string


async def called_once_a_day():  # Fired every day
    print("online")
    await bot.wait_until_ready()  # Make sure your guild cache is ready so the channel can be found via get_channel
    channel = bot.get_channel(channel_id) # Note: It's more efficient to do bot.get_guild(guild_id).get_channel(channel_id) as there's less looping involved, but just get_channel still works fine
    await channel.send(f"Alarme iniciado")
    print(len(lista_materias))
    for materias in lista_materias:
        if len(materias.provas) > 0:
            for prova in materias.provas:
                # print(f"A prova de {prova.nomeProva} da matéria {materias.nomeMateria} é daqui a {checarData(prova.data)} dias")
                if not saber_se_data_prova_ja_passou(prova.data):
                    if checarData(prova.data) == 1:
                        await channel.send(f"A prova de {prova.nomeProva} da matéria {materias.nomeMateria} é amanhã")
                    elif checarData(prova.data) == 0:
                        await channel.send(f"A prova de {prova.nomeProva} da matéria {materias.nomeMateria} é hoje")
                    elif checarData(prova.data) == 7:
                        await channel.send(f"A prova de {prova.nomeProva} da matéria {materias.nomeMateria} é daqui a uma semana")
                    elif checarData(prova.data) == 14:
                        await channel.send(f"A prova de {prova.nomeProva} da matéria {materias.nomeMateria} é daqui a duas semanas")
                    else:
                        await channel.send(f"A prova de {prova.nomeProva} da matéria {materias.nomeMateria} é daqui a {checarData(prova.data)} dias")
    #await channel.send("This is a timed notification!")

def removerMateria():
    pass

def emoji_to_boolean(emoji):
    match emoji:
        case '👍':
            return True
        case _:
            return False

def emoji_to_att(emoji):
    
    pass

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

def number_to_unicode(texto):
    match texto:
        case 0:
            return "0️⃣"
        case 1:
            return "1️⃣"
        case 2:
            return "2️⃣"
        case 3:
            return "3️⃣"
        case 4:
            return "4️⃣"
        case 5:
            return "5️⃣"
        case 6:
            return "6️⃣"
        case 7:
            return "7️⃣"
        case 8:
            return "8️⃣"
        case 9:
            return "9️⃣"
        case 10:
            return "🔟"

def perguntaMateria():
    strPerguntas = ''
        
    emojis = ["0️⃣","1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣","8️⃣","9️⃣","🔟"]
    opcoesAtuais = []
        
    for i, mat in enumerate(lista_materias):
        strPerguntas += f'{emojis[i]} - {mat.nomeMateria}\n'
        opcoesAtuais.append(emojis[i])
    return strPerguntas, opcoesAtuais

def pegarIndiceMateria(materiaAux: Materia):
    for i, materia in enumerate(lista_materias):
        if materiaAux.nomeMateria.upper() == materia.nomeMateria.upper():
            return i
    return -1

async def pegarMateriasDeletadas(message, materias):
    manterPergunta = True
    while manterPergunta:
        emoji = await perguntar(message, "Deseja remover uma materia")
        deseja = emoji_to_boolean(emoji)
        if deseja:
            strPergunta, opcoesAtuais = perguntaMateria()
            materiaEmoji = await perguntar(message, strPergunta, opcoesAtuais)
            materiaAtual = unicode_to_number(materiaEmoji)
            print(materiaAtual)
            materiaObj = materias[int(materiaAtual)]
            indice = pegarIndiceMateria(materiaObj)
            del lista_materias[indice]
        else:
            manterPergunta = False

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

async def alarmeProvas():
    pass

async def miguis(message, miguez):
    emoji = '<:miguezjoker:821111485564452944>'
    await message.add_reaction(emoji)

async def perguntar(mensagem, nome, opcoes: tuple[str]=('👍', '👎')):
    message = mensagem
    await message.channel.send(nome)
    
    msg = await message.channel.fetch_message(message.channel.last_message_id) ##TODO: fazer com que seja a mensagem certa, não só a última pois isso é inconsistente
    
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

def join_conteudos(conteudos: list[str]):
    stringFormatada = ''
    tamanhocont = len(conteudos)
    for i, cont in enumerate(conteudos):
        stringFormatada += f'{cont},'
    return stringFormatada


@bot.event
async def on_ready():
    print(f'Estou pronto -> {bot.user}')

@bot.group(invoke_without_command=True)
async def ajuda(ctx):
    em = discord.Embed(title="Ajuda", description="Use >ajuda <extend> para extender a syntax de um comando", color=ctx.author.color)
    em.add_field(name="Prova", value="`pararalarme`\n  `alarme`\n  `saberpassou`\n `addprova`\n`addconteudo`\n `addmateria`\n `editarprova`\n `removermateria`\n`removerprova`\n `removertodasasprovas`\n `printarprovas`\n `salvar`\n `carregar`\n `aula`\n")
    em.add_field(name="Extras", value="`miguez`\n `rafik`\n `lipao`\n `nandin`")
    await ctx.send(embed=em)


@ajuda.command()
async def saberpassou(ctx):
    em = discord.Embed(title="Saber se passou", description="Verifique se voce passou direto ou precisa ir para final", color=ctx.author.color)
    em.add_field(name="**Sintaxe**", value=">saberpassou")
    await ctx.send(embed=em)

@ajuda.command()
async def pararalarme(ctx):
    em = discord.Embed(title="Parar Alarme", description="Para o alarme", color=ctx.author.color)
    em.add_field(name="**Sintaxe**", value=">pararalarme")
    await ctx.send(embed=em)

@ajuda.command()
async def alarme(ctx):
    em = discord.Embed(title="Alarme", description="Inicia o alarme das provas, todo dia as 20 horas ele pinga quantos dias faltam", color=ctx.author.color)
    em.add_field(name="**Sintaxe**", value=">alarme")
    await ctx.send(embed=em)

@ajuda.command()
async def addprova(ctx):
    em = discord.Embed(title="AddProva", description="Adiciona uma prova em alguma materia", color=ctx.author.color)
    em.add_field(name="**Sintaxe**", value=">addprova") 
    await ctx.send(embed=em)

@ajuda.command()
async def addconteudo(ctx):
    em = discord.Embed(title="AddConteudo", description="Adiciona uma lista de conteudos numa prova de uma materia", color=ctx.author.color)  
    em.add_field(name="**Sintaxe**", value=">addconteudo")
    await ctx.send(embed=em)

@ajuda.command()
async def addmateria(ctx):
    em = discord.Embed(title="AddMateria", description="Adiciona uma nova materia", color=ctx.author.color)
    em.add_field(name="**Sintaxe**", value=">addmateria")
    await ctx.send(embed=em)

@ajuda.command()
async def editarprova(ctx):
    em = discord.Embed(title="EditarProva", description="Edite os atributos(nota, data, nome, conteudos, unidade) de uma prova", color=ctx.author.color)
    em.add_field(name="**Sintaxe**", value=">editarprova")
    await ctx.send(embed=em)

@ajuda.command()
async def removermateria(ctx):
    em = discord.Embed(title="RemoverMateria", description="Remove uma materia da lista de materias", color=ctx.author.color)
    em.add_field(name="**Sintaxe**", value=">removermateria")
    await ctx.send(embed=em)

@ajuda.command()
async def removerprova(ctx):
    em = discord.Embed(title="RemoverProva", description="Remove uma prova de uma materia", color=ctx.author.color)
    em.add_field(name="**Sintaxe**", value=">removerprova")
    await ctx.send(embed=em)

@ajuda.command()
async def removertodasasprovas(ctx):
    em = discord.Embed(title="RemoverTodasAsProvas", description="Remove todas as provas de uma materia", color=ctx.author.color)
    em.add_field(name="**Sintaxe**", value=">removertodasasprovas")
    await ctx.send(embed=em)

@ajuda.command()
async def printarprovas(ctx):
    em = discord.Embed(title="PrintarProvas", description="Lista as provas de todas as materias", color=ctx.author.color)
    em.add_field(name="**Sintaxe**", value=">printarprovas")
    await ctx.send(embed=em)

@ajuda.command()
async def salvar(ctx):
    em = discord.Embed(title="Salvar", description="Salva a lista de materias num JSON", color=ctx.author.color)
    em.add_field(name="**Sintaxe**", value=">salvar")
    await ctx.send(embed=em)

@ajuda.command()
async def carregar(ctx):
    em = discord.Embed(title="Carregar", description="Carrega a lista de materias de um JSON", color=ctx.author.color)
    em.add_field(name="**Sintaxe**", value=">carregar")
    await ctx.send(embed=em)

@ajuda.command()
async def aula(ctx):
    em = discord.Embed(title="Aula", description="Verifique onde vai ser sua aula", color=ctx.author.color)
    em.add_field(name="**Sintaxe**", value=">aula")
    await ctx.send(embed=em)

@ajuda.command()
async def miguez(ctx):
    em = discord.Embed(title="Miguez", description="Xingue Miguez", color=ctx.author.color)
    em.add_field(name="**Sintaxe**", value=">miguez")
    await ctx.send(embed=em)

@ajuda.command()
async def rafik(ctx):
    em = discord.Embed(title="Rafik", description="Só o Básico",color=ctx.author.color)
    em.add_field(name="**Sintaxe**", value=">rafik")
    await ctx.send(embed=em)

@ajuda.command()
async def lipao(ctx):
    em = discord.Embed(title="Lipao", description="HeteroTop, Maromba, Popó da nova geração", color=ctx.author.color)
    em.add_field(name="**Sintaxe**", value=">lipao")
    await ctx.send(embed=em)

@ajuda.command()
async def nandin(ctx):
    em = discord.Embed(title="Nandin", description="Laranja inutil", color=ctx.author.color)
    em.add_field(name="**Sintaxe**", value=">nandin")
    await ctx.send(embed=em)

@bot.event
async def on_message(message):
    comp = bot.get_guild(int(config['COMP']))
    miguez = comp.get_member(int(config['MIGUEZ']))
    nandin = comp.get_member(int(config['NANDIN']))
    lipao = comp.get_member(int(config['LIPAO']))
    lion = comp.get_member(int(config['LION']))
    rafik = comp.get_member(int(config['RAFIK']))
    #drungas = comp.get_member(int(config['DRUNGAS']))
    if message.author.id == miguez.id:
        chance = randint(1,10)
        if chance == 1:
            await miguis(message, miguez)
    if message.author == bot.user:
        return
    if message.content.lower().startswith('>pararalarme'):
        lembrete.stop()
        await message.channel.send('Alarme foi parado')
    if message.content.lower().startswith('>alarme'):
        lembrete.start()
    if message.content.lower().startswith('>nandin'):
        await message.channel.send(f'Esse é o laranjinha ?{nandin.mention}KKKKKKKKKKKKKKKK. Muito idiota!')
    if message.content.lower().startswith('>lipao'):
        await message.channel.send(f'{lipao.mention} Cada dia que passa, eu fico mais decepcionado com voce. Olhe a porra do wpp mermao !')
        await message.channel.send('E nem adianta vc pedir pra ir na mão, vc é um fracote que nao merece meu tempo!')
    if message.content.lower().startswith('>rafik'):
        await message.channel.send(F"{rafik.mention} Só o Básico!")
    if message.content.lower().startswith('>addmateria'):
        materia =  await perguntar_texto(message, "Por favor digite o nome da matéria:")
        materiaObj = Materia(materia)
        tem = Materia.buscarMateria(lista_materias, materiaObj.nomeMateria)
        if tem:
            await message.channel.send("Matéria Já existe")
            return
        lista_materias.append(materiaObj)
        await message.channel.send(f"Materia: {materia} adicionado com sucesso")
    if message.content.lower().startswith('>addprova'):        
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

    if message.content.lower().startswith('>addconteudo'):

        strPerguntas, opcoesAtuais = perguntaMateria()
        resposta = await perguntar(message, strPerguntas, opcoesAtuais)
        materiaAtual = unicode_to_number(resposta)
        materiaObj = lista_materias[int(materiaAtual)]

        provas = materiaObj.provas
        strmensagem = ""
        opcoesprovas = []
        for i, cont in enumerate(provas):
            strmensagem = strmensagem + number_to_unicode(i) + " - " + cont.nomeProva + "\n"
            opcoesprovas.append(number_to_unicode(i))

       

        nomeProva = provas[unicode_to_number(await perguntar(message,strmensagem,opcoesprovas))].nomeProva
        conteudos = await perguntarConteudo(message)
        
        conteudosFormatado = join_conteudos(conteudos)
        print(conteudosFormatado)
        operacaoConcluida = materiaObj.adicionarConteudoNumaProva(conteudosFormatado, nomeProva)
        if not operacaoConcluida[0]:
            await message.channel.send(operacaoConcluida[1])
            return
        await message.channel.send(operacaoConcluida[1])
    
    if message.content.lower().startswith('>removerprova'):
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
    
    if message.content.lower().startswith('>removertodasasprovas'):
        strPerguntas, opcoesAtuais = perguntaMateria()
        resposta = await perguntar(message, strPerguntas, opcoesAtuais)
        materiaAtual = unicode_to_number(resposta)
        materiaObj = lista_materias[int(materiaAtual)]
        req, msg = materiaObj.removerTodasAsProvas()
        if not req:
            await message.channel.send(msg)
            return
        await message.channel.send(msg)

    if message.content.lower().startswith('>salvar'):
        with open('dados.json', 'w') as f:
            table = []
            for materias in lista_materias:
                table.append(materias.to_dict())
            json.dump(table, f)
        await message.channel.send('Salvado com sucesso')

    if message.content.lower().startswith('>carregar'):
       with open('dados.json', 'r') as f:
        table = json.load(f)
        provaObj = None
        for obj in table:
            provas = []
            for prova in obj['provas']:
                provaObj = Prova(unidade=prova['unidade'], data=prova['data'], nomeProva=prova['nomeProva'], notaProva=prova['notaProva'])
                provaObj.setConteudos(prova['conteudos'])
                provas.append(provaObj)
            materia = Materia(obj['nomeMateria'])
            materia.setProvas(provas)
            lista_materias.append(materia)
       await message.channel.send('Carregado com sucesso')

    if message.content.lower().startswith('>removermateria'):
       await pegarMateriasDeletadas(message, lista_materias) 

    if message.content.lower().startswith('>editarprova'):
        strPerguntas, opcoesAtuais = perguntaMateria()
        materia = await perguntar(message, strPerguntas, opcoesAtuais)
        materiaIndex = unicode_to_number(materia)
        materiaObj = lista_materias[int(materiaIndex)]

        provas = materiaObj.provas
        strmensagem = ""
        opcoesprovas = []
        for i, cont in enumerate(provas):
            strmensagem = strmensagem + number_to_unicode(i) + " - " + cont.nomeProva + "\n"
            opcoesprovas.append(number_to_unicode(i))

       

        nomeProva = provas[unicode_to_number(await perguntar(message,strmensagem,opcoesprovas))].nomeProva

        prova = materiaObj.procurarProva(nomeProva)
        if not prova:
            await message.channel.send("Prova não existe")
            return
        opcoesAtuais = ('📅', '🔢', '🔟', '🔤', '📦')
        strPerguntas = "Qual atributo voce quer editar ?\n"
        for i in opcoesAtuais:
            match i:
                case '📅':
                    strPerguntas += f'{i} - Data\n'
                case '🔢':
                    strPerguntas += f'{i} - Unidade\n'
                case '🔟':
                    strPerguntas += f'{i} - Nota\n'
                case '🔤':
                    strPerguntas += f'{i} - Nome\n'
                case '📦':
                    strPerguntas += f'{i} - Conteudos\n'
            
        emoji = await perguntar(message, strPerguntas,('📅', '🔢', '🔟', '🔤', '📦'))
        if emoji == '🔢':
            unidade = await perguntar(message, "Escolha a unidade da prova", ("1️⃣","2️⃣","3️⃣","4️⃣"))
            prova.unidade = unicode_to_number(unidade)
        elif emoji == '📦' and len(prova.conteudos) > 0:
            conteudos = prova.conteudos
            strmensagem = ""
            opcoesconteudo = []
            for i, cont in enumerate(conteudos):
                strmensagem = strmensagem + number_to_unicode(i) + " - " + cont + "\n"
                opcoesconteudo.append(number_to_unicode(i))

            conteudoescolha = await perguntar(message, strmensagem, opcoesconteudo)
            
            if conteudoescolha and opcoesconteudo[unicode_to_number(conteudoescolha)]: 
                conteudoEditado = await perguntar_texto(message, "Ok, por favor informe o novo conteudo.")
                if conteudoEditado:
                    prova.removerConteudo(prova.conteudos[unicode_to_number(conteudoescolha)])
                    prova.adicionarConteudo(conteudoEditado)
        elif emoji == '📦' and len(prova.conteudos) <= 0:
            await message.channel.send("Não há conteúdos para serem editados. Adicione conteúdos com `>AddConteudo`")
            
        elif emoji == '📅':
            data = await perguntar_texto(message, "Qual a nova data da prova ?")
            prova.data = data
            await message.channel.send("Data atualizada")
        
        elif emoji == "🔟":
            nota = await perguntar_texto(message, "Qual a nova nota da prova ?")
            prova.notaProva= nota
            await message.channel.send("Nota atualizada")

        elif emoji == "🔤":
            nome = await perguntar_texto(message, "Qual o novo nome da prova ?")
            prova.nomeProva= nome
            await message.channel.send("Nome atualizado")

    if message.content.lower().startswith('>miguez'):
        await message.channel.send(f'{miguez.mention} podre!')
    
    if message.content.lower().startswith('>printarprovas'):
        msg = Materia.printarMaterias(lista_materias)
        await message.channel.send(msg)
    
    if message.content.lower().startswith('>aula'):
        ra =  await perguntar_texto(message, "Digite seu RA(com ponto):")
        print(ra)
        aulas = pegarSalas(ra)
        await message.channel.send(aulas)
    
    if message.content.lower().startswith('>saberpassou'):
        av1 =  await perguntar_texto(message, "Digite media av1:")
        av1 = float(av1)
        av2 =  await perguntar_texto(message, "Digite media av2:")
        av2 = float(av2)
        av3 =  await perguntar_texto(message, "Digite media av3:")
        av3 = float(av3)
        edag =  await perguntar_texto(message, "Digite media edag:")
        edag = float(edag)
        media = av1*0.25 + av2*0.25 +av3*0.3 + edag*0.2
        await message.channel.send(f'Sua média esta {media}')
        unidade = await perguntar(message, "Ja terminou as unidades ?")
        deseja = emoji_to_boolean(unidade)
        if deseja:
            if media < 1.7:
                await message.channel.send(f'Infelizmente tu perdeu meu bom 😞')
            elif media >= 1.7 and media < 7:
                media = round(media, 1)
                await message.channel.send(f'Tu precisa de {dic_final[media]} na final para passar')
            else:
                await message.channel.send('Parabeeeeens esta de ferias')
        else:
            if media < 7: 
                await message.channel.send('Assumindo q so falta a 3° unidade')
                falta = (7 - media) / 0.3
                await message.channel.send(f'tu falta {falta} para passar')
            else:
                await message.channel.send('Parabeeeeens esta de ferias sem final')
            
    await bot.process_commands(message)

def seconds_until(hours, minutes):
    given_time = datetime.time(hours, minutes)
    now = datetime.datetime.now()
    future_exec = datetime.datetime.combine(now, given_time)
    if (future_exec - now).days < 0:  # If we are past the execution, it will take place tomorrow
        future_exec = datetime.datetime.combine(now + datetime.timedelta(days=1), given_time) # days always >= 0

    return (future_exec - now).total_seconds()

@tasks.loop(hours=1)
async def lembrete():
    if datetime.now().hour == 20:
        await called_once_a_day()

bot.run(config['TOKEN'])