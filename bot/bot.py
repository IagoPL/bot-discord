import discord
import requests
import os
from discord.ext import commands
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
API_URL = os.getenv("API_URL")

# Configuración del bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Comando para crear una votación
@bot.command(name='crear_votacion')
async def crear_votacion(ctx, pregunta: str, *opciones):
    if len(opciones) < 2:
        await ctx.send("Necesitas al menos dos opciones para crear una votación.")
        return

    payload = {
        "pregunta": pregunta,
        "opciones": list(opciones),
        "canal_id": ctx.channel.id,
        "servidor_id": ctx.guild.id
    }

    response = requests.post(f"{API_URL}/crear_votacion", json=payload)

    if response.status_code == 200:
        await ctx.send(f"Votación creada: {pregunta}")
    else:
        await ctx.send("Hubo un problema al crear la votación.")

# Comando para añadir un voto
@bot.command(name='votar')
async def votar(ctx, votacion_id: int, opcion: str):
    payload = {
        "votacion_id": votacion_id,
        "voto": opcion
    }

    response = requests.post(f"{API_URL}/añadir_voto", json=payload)

    if response.status_code == 200:
        await ctx.send(f"Voto registrado para la opción: {opcion}")
    else:
        await ctx.send("Hubo un problema al registrar tu voto. Asegúrate de que la opción sea válida.")

# Comando para mostrar los resultados de una votación
@bot.command(name='resultados')
async def resultados(ctx, votacion_id: int):
    response = requests.get(f"{API_URL}/mostrar_votacion/{votacion_id}")

    if response.status_code == 200:
        data = response.json()
        resultados = "\n".join([f"{opcion}: {votos} votos" for opcion, votos in data["resultados"].items()])
        await ctx.send(f"Resultados para la votación: {data['pregunta']}\n{resultados}")
    else:
        await ctx.send("No se pudieron obtener los resultados de la votación.")

# Iniciar el bot
bot.run(TOKEN)
