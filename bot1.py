import discord
from discord.ext import commands
import os
import yt_dlp

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Opciones mejoradas de yt-dlp (ANTI BLOQUEO)
ytdl_format_options = {
    'format': 'bestaudio/best',
    'quiet': True,
    'noplaylist': True,
    'extract_flat': False,
    'source_address': '0.0.0.0',
    'nocheckcertificate': True,
    'ignoreerrors': True
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

# JOIN
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()
        await ctx.send("Me uní al canal ✅")
    else:
        await ctx.send("Tenés que estar en un canal de voz ❌")

# PLAY (FIX YOUTUBE)
@bot.command()
async def play(ctx, url):
    if not ctx.author.voice:
        await ctx.send("Tenés que estar en un canal de voz ❌")
        return

    channel = ctx.author.voice.channel

    if ctx.voice_client is None:
        await channel.connect()

    vc = ctx.voice_client

    try:
        info = ytdl.extract_info(url, download=False)

        if info is None:
            await ctx.send("No se pudo obtener el audio ❌")
            return

        # Si es playlist
        if 'entries' in info:
            info = info['entries'][0]

        url2 = info.get('url')

        if not url2:
            await ctx.send("No se encontró el audio ❌")
            return

        source = discord.FFmpegPCMAudio(url2, **ffmpeg_options)

        vc.stop()
        vc.play(source)

        await ctx.send("Reproduciendo 🎶")

    except Exception as e:
        await ctx.send(f"Error al reproducir ❌")
        print("ERROR:", e)

# STOP
@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.send("Música detenida ⏹")
    else:
        await ctx.send("No estoy reproduciendo nada ❌")

# LEAVE
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Salí del canal 👋")
    else:
        await ctx.send("No estoy en ningún canal ❌")

# TOKEN
token = os.environ["DISCORD_TOKEN"]
bot.run(token)
