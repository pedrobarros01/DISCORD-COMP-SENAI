import discord
from discord.ext import commands
from dotenv import dotenv_values
config = dotenv_values(".env")
print(config['TOKEN'])
intents = discord.Intents.all()
bot = commands.Bot(">", intents=intents)

@bot.event
async def on_ready():
    print(f'Estou pronto -> {bot.user}')

@bot.event
async def on_message(message):
    print(f'Estou pronto -> {bot.user}')

@bot.command(name="oi")
async def mandar_oi(ctx):
    name = ctx.author.name
    conteudo = ctx.message
    resposta = "Olá, " + name
    resposta2 = f"Voce digitou: {conteudo}"
    await ctx.send(resposta2)

bot.run(config['TOKEN'])