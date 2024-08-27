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
    
    # Crear la votación a través de la API
    data = {
        "pregunta": pregunta,
        "opciones": opciones
    }
    response = requests.post("http://localhost:5000/api/crear_votacion", json=data)
    
    if response.status_code == 200:
        votacion = response.json()
        opciones_texto = "\n".join([f"{i+1}. {op}" for i, op in enumerate(opciones)])
        mensaje = await ctx.send(f"**{pregunta}**\n\n{opciones_texto}")
        
        # Agregar reacciones para votar
        for i in range(len(opciones)):
            await mensaje.add_reaction(f"{i+1}\u20E3")
        
        # Actualizar la votación con el mensaje de Discord
        votacion_id = votacion["id"]
        data_update = {
            "mensaje_id": mensaje.id,
            "canal_id": ctx.channel.id,
            "servidor_id": ctx.guild.id
        }
        update_response = requests.put(f"http://localhost:5000/api/actualizar_votacion/{votacion_id}", json=data_update)
        
        if update_response.status_code == 200:
            await ctx.send("Votación creada exitosamente y guardada en la base de datos.")
        else:
            await ctx.send("Hubo un error al intentar actualizar la votación en la base de datos.")
    else:
        await ctx.send("Hubo un error al intentar crear la votación en la base de datos.")

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    
    mensaje_id = reaction.message.id
    voto = reaction.emoji[0]
    
    if voto.isdigit():
        data = {
            "votacion_id": mensaje_id,
            "voto": int(voto)
        }
        response = requests.post("http://localhost:5000/api/añadir_voto", json=data)
        
        if response.status_code == 200:
            await reaction.message.channel.send(f"Voto registrado: {voto}")
        else:
            await reaction.message.channel.send(f"Hubo un error al registrar el voto: {response.json().get('message', 'Error desconocido')}")

@bot.command(name='resultados')
async def resultados(ctx, votacion_id: int):
    response = requests.get(f"http://localhost:5000/api/mostrar_votacion/{votacion_id}")
    
    if response.status_code == 200:
        votacion = response.json()
        opciones = votacion["opciones"]
        resultados = votacion["resultados"]
        resultado_texto = "\n".join([f"{opcion}: {resultados[opcion]} votos" for opcion in opciones])
        await ctx.send(f"Resultados de la votación:\n{resultado_texto}")
    else:
        await ctx.send(f"No se pudo obtener los resultados: {response.json().get('message', 'Error desconocido')}")

# Inicia el bot usando el token cargado desde la variable de entorno
bot.run(DISCORD_TOKEN)
