import asyncio
import discord
from Materia import Materia
from discord.ext import commands
from datetime import datetime, time, timedelta
import json
from discord.ext import tasks
from dotenv import dotenv_values
from random import randint
from Prova import Prova
config = dotenv_values(".env")
intents = discord.Intents.all()
bot = commands.Bot(">", intents=intents)
lista_materias: list[Materia] = []

def checarData(data):
    data = data.split('/')
    if len(data) == 2:
        data.append(str(datetime.now().year))
    elif len(data) != 3:
        return False
    
    delta = datetime(day=int(data[0]), month=int(data[1]), year=int(data[2])) - datetime.now()
    return delta.days + 1

WHEN = time(19, 18, 40)  # 6:00 PM
channel_id = 0 # CANAL DE AVISO DE PROVAS # bot.run(config['CANAL']) (?) #

def carregar():
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

async def called_once_a_day():  # Fired every day
    print("online")
    await bot.wait_until_ready()  # Make sure your guild cache is ready so the channel can be found via get_channel
    channel = bot.get_channel(channel_id) # Note: It's more efficient to do bot.get_guild(guild_id).get_channel(channel_id) as there's less looping involved, but just get_channel still works fine
    print(len(lista_materias))
    for materias in lista_materias:
        if len(materias.provas) > 0:
            for prova in materias.provas:
                print(f"A prova de {prova.nomeProva} da matéria {materias.nomeMateria} é daqui a {checarData(prova.data)} dias")
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

async def background_task():
    now = datetime.utcnow()
    if now.time() > WHEN:  # Make sure loop doesn't start after {WHEN} as then it will send immediately the first time as negative seconds will make the sleep yield instantly
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
        await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start 
    while True:
        now = datetime.utcnow() # You can do now() or a specific timezone if that matters, but I'll leave it with utcnow
        target_time = datetime.combine(now.date(), WHEN)  # 6:00 PM today (In UTC)
        seconds_until_target = (target_time - now).total_seconds()
        await asyncio.sleep(seconds_until_target)  # Sleep until we hit the target time
        await called_once_a_day()  # Call the helper function that sends the message
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
        await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start a new iteration

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



async def miguis(message, miguez):
    emoji = '🤡'
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
    lembrete.start()
    carregar()

@bot.event
async def on_message(message):
#    comp = bot.get_guild(int(config['COMP']))
#    miguez = comp.get_member(int(config['MIGUEZ']))
#    if message.author.id == miguez.id:
#        await miguis(message, miguez)
    if message.author == bot.user:
        return
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

    if message.content.lower().startswith('>yn'):
        resposta = await perguntar_texto(message, "Pergunta exemplo")
        print(resposta)

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

    if message.content.lower().startswith('>carregar'):
       carregar()


    if message.content.lower().startswith('>removerMateria'):
       await pegarMateriasDeletadas(message, lista_materias) 

    if message.content.lower().startswith('>editarProva'):
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
        comp = bot.get_guild(677252577611612170)
        miguez = comp.get_member(204386578414436352)
        await message.channel.send(f'{miguez.mention} podre!')
    
    if message.content.lower().startswith(">ajuda") or message.content.lower().startswith(">help"):
        await message.channel.send("""```>ajuda; >help
>AddProva
>EditarProva
>AddMateria
>AddConteudo
>RemoverMateria 
>Miguez```""")
    
    if message.content.lower().startswith('>printarprovas'):
        msg = Materia.printarMaterias(lista_materias)
        await message.channel.send(msg)
    '''if message.content.lower().startswith('>miguez'):
        comp = bot.get_guild(991739407314984990)s
        miguez = comp.get_member(796901549506166864)
        await miguez.kick()'''

def seconds_until(hours, minutes):
    given_time = datetime.time(hours, minutes)
    now = datetime.datetime.now()
    future_exec = datetime.datetime.combine(now, given_time)
    if (future_exec - now).days < 0:  # If we are past the execution, it will take place tomorrow
        future_exec = datetime.datetime.combine(now + datetime.timedelta(days=1), given_time) # days always >= 0

    return (future_exec - now).total_seconds()

@tasks.loop(minutes=35)
async def lembrete():
    if datetime.now().hour == 20:
        await called_once_a_day()



bot.run(config['TOKEN'])