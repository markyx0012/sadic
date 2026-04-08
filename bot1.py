import discord
from discord.ext import commands
import wavelink
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Conectar a Lavalink
@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

    try:
        node = wavelink.Node(
            uri="http://lava.link:80",
            password="anything"
        )

        await wavelink.Pool.connect(client=bot, nodes=[node])
        print("✅ Conectado a Lavalink")

    except Exception as e:
        print("❌ Error conectando a Lavalink:", e)
        
# JOIN
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect(cls=wavelink.Player)
        await ctx.send("Conectado al canal ✅")
    else:
        await ctx.send("Entrá a un canal de voz ❌")

# PLAY
@bot.command()
async def play(ctx, *, search: str):
    if not ctx.author.voice:
        await ctx.send("Entrá a un canal de voz ❌")
        return

    vc: wavelink.Player

    if not ctx.voice_client:
        vc = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    else:
        vc = ctx.voice_client

    tracks = await wavelink.Playable.search(search)

    if not tracks:
        await ctx.send("No encontré nada ❌")
        return

    track = tracks[0]

    await vc.play(track)
    await ctx.send(f"Reproduciendo 🎶: {track.title}")

# STOP
@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.stop()
        await ctx.send("Detenido ⏹")
    else:
        await ctx.send("Nada reproduciendo ❌")

# LEAVE
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Me fui 👋")
    else:
        await ctx.send("No estoy en VC ❌")

# TOKEN
bot.run(os.environ["DISCORD_TOKEN"])
