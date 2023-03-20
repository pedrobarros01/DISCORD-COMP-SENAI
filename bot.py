import discord
from discord.ext import commands
from dotenv import dotenv_values
config = dotenv_values(".env")
print(config['TOKEN'])
intents = discord.Intents.all()
bot = commands.Bot(">", intents=intents)
lista_provas = []
@bot.event
async def on_ready():
    print(f'Estou pronto -> {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('>AddProva'):
        prova = message.content.split('>AddProva')[1]
        lista_provas.append(prova)
        await message.channel.send("Prova adicionado com sucesso")
    if message.content.startswith('>miguez'):
        comp = bot.get_guild()
        miguez = comp.get_member()
        await miguez.kick()

bot.run(config['TOKEN'])