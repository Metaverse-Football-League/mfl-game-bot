import teams.commands
from config import config
from discord_bot import bot
import discord

#### CREATE TEAM ####
# Usage: !create
@bot.command(name='create', description='The first step to enter into the game...')
async def create_team(ctx):
    if str(ctx.channel.id) in config["gameChan"]:
        await teams.commands.create_team(ctx)

#### VIEW TEAM ####
# Usage: !view <@User>
@bot.command(name='view')
async def view_team(ctx, user: discord.User):
    if str(ctx.channel.id) in config["gameChan"]:
        await teams.commands.view_team(ctx, user)
