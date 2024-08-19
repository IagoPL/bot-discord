import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener el token del bot desde las variables de entorno
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Configura el prefijo de comandos y los intents necesarios
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} ha iniciado sesión.')

@bot.command(name='votar')
async def votar(ctx, pregunta: str, *opciones):
    if len(opciones) < 2:
        await ctx.send('Debes proporcionar al menos dos opciones para la votación.')
        return
    
    opciones_texto = "\n".join([f"{i+1}. {op}" for i, op in enumerate(opciones)])
    mensaje = await ctx.send(f"**{pregunta}**\n\n{opciones_texto}")
    
    for i in range(len(opciones)):
        await mensaje.add_reaction(f"{i+1}\u20E3")
    
    data = {
        "pregunta": pregunta,
        "opciones": opciones,
        "mensaje_id": mensaje.id,
        "canal_id": ctx.channel.id,
        "servidor_id": ctx.guild.id
    }
    response = requests.post("http://api.com/crear_votacion", json=data)  # Reemplaza con tu URL real
    
    if response.status_code == 200:
        await ctx.send("Votación creada exitosamente y guardada en la base de datos.")
    else:
        await ctx.send("Hubo un error al intentar guardar la votación en la base de datos.")

@bot.command(name='cerrar_votacion')
async def cerrar_votacion(ctx, mensaje_id: int):
    mensaje = await ctx.fetch_message(mensaje_id)
    reacciones = mensaje.reactions
    resultados = {}
    
    for reaccion in reacciones:
        if reaccion.emoji.isdigit():
            resultados[int(reaccion.emoji[0])] = reaccion.count - 1
    
    resultado_texto = "\n".join([f"Opción {key}: {value} votos" for key, value in resultados.items()])
    await ctx.send(f"Resultados de la votación:\n{resultado_texto}")
    
    data = {
        "mensaje_id": mensaje_id,
        "resultados": resultados
    }
    response = requests.post("http://api.com/cerrar_votacion", json=data)  # Reemplaza con tu URL real
    
    if response.status_code == 200:
        await ctx.send("Resultados guardados exitosamente en la base de datos.")
    else:
        await ctx.send("Hubo un error al intentar guardar los resultados en la base de datos.")

# Inicia el bot usando el token cargado desde la variable de entorno
bot.run(DISCORD_TOKEN)
