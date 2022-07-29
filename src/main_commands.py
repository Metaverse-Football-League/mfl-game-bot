from random import randint
import teams
import players
from config import config
from discord_bot import bot
import discord

f_teams = config["dataPath"] + "teams.csv"

#### CREATE TEAM ####
# Usage: !create
@bot.command(name='create', description='The first step to enter into the game...')
async def create_team(ctx):
    if str(ctx.channel.id) in config["gameChan"]:
        with open(f_teams, "r+") as tfile:
            user = ctx.interaction.user
            user_id = str(user.id)
            if user.id > 1000000: # if it's not for a bot
                username = user.name if user.nick is None else user.nick
                team_name = "FC "+ username
            else:
                username = "BOT"
            team_id = user_id
            if user_id in tfile.read():
                if str(user_id) in config["adminId"]:
                    team_id = str(randint(1, 999999))
                    team_name = "Team"+str(randint(1,1000))
                    tfile.write(team_name + "," + team_id + ",no,3,BOT,\n")
                    await players.create(team_id, username)
                    await ctx.respond("Team " + team_name + " created !", ephemeral=True)
                else:
                    await ctx.respond("Sorry, you already have a team !", ephemeral=True)
            else:
                tfile.write(team_name + "," + team_id + ",yes,3,"+username+"\n")
                await players.create(team_id, username)
                await ctx.respond("Team " + team_name + " created !", ephemeral=True)

#### VIEW TEAM ####
# Usage: !view <@User>
@bot.command(name='view')
async def view_team(ctx, user: discord.User):
    if str(ctx.channel.id) in config["gameChan"]:
        embed_team = await teams.getAll(str(user.id))
        await ctx.respond(embed=embed_team, ephemeral=False)
