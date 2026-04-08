import discord
from discord.ext import commands
import os
import yt_dlp

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Opciones de yt-dlp
ytdl_format_options = {
    'format': 'bestaudio/best',
    'quiet': True
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

# Unirse al canal
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

# Reproducir música
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
        with ytdl.extract_info(url, download=False) as info:
            url2 = info['url']
            source = discord.FFmpegPCMAudio(url2, **ffmpeg_options)

            vc.stop()
            vc.play(source)

        await ctx.send("Reproduciendo 🎶")

    except Exception as e:
        await ctx.send(f"Error al reproducir ❌: {e}")

# Detener música
@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.send("Música detenida ⏹")
    else:
        await ctx.send("No estoy reproduciendo nada ❌")

# Salir del canal
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Salí del canal 👋")
    else:
        await ctx.send("No estoy en ningún canal ❌")

# Token
token = os.environ["DISCORD_TOKEN"]
bot.run(token)
