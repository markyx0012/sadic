import discord
import json
import asyncio
import yt_dlp
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True

bot = discord.Client(intents=intents)

with open("config.json") as f:
    config = json.load(f)

guild_id = config["guild_id"]
voice_channel_id = config["voice_channel_id"]
playlist = config["mix"]

YDL_OPTIONS = {
    "format": "bestaudio",
    "quiet": True,
    "noplaylist": True
}

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn"
}

current_index = 0
voice_client = None


async def play_loop():
    global current_index, voice_client

    await bot.wait_until_ready()

    guild = bot.get_guild(guild_id)
    if guild is None:
        print("No se encontró el servidor")
        return

    channel = guild.get_channel(voice_channel_id)
    if not isinstance(channel, discord.VoiceChannel):
        print("Canal de voz inválido")
        return

    try:
        voice_client = await channel.connect()
    except Exception as e:
        print(f"Error al conectar: {e}")
        return

    while True:
        try:
            url = playlist[current_index]

            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                audio_url = info["url"]

            source = discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS)
            voice_client.play(source)

            while voice_client.is_playing():
                await asyncio.sleep(1)

            current_index = (current_index + 1) % len(playlist)

        except Exception as e:
            print(f"Error en reproducción: {e}")
            await asyncio.sleep(5)


@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    # asyncio.create_task(play_loop())


import os

token = os.getenv("DISCORD_TOKEN")

if not token:
    raise Exception("No se encontró el token")

bot.run(token)
