from random import randint
import teams.service
import players.service
from config import config
import discord

async def create_team(ctx):
    user = ctx.interaction.user
    user_id = str(user.id)

    if user.id > 1000000: # if it's not for a bot
        coach_name = user.name if user.nick is None else user.nick
        team_id = user_id
        team_name = "FC " + coach_name
    else:
        coach_name = "BOT"
        team_id = str(randint(1, 999999))
        team_name = "Team" + str(randint(1,1000))

    if await teams.service.get_by_id(team_id) is None:
        await teams.service.create(team_name, team_id, "yes", "3", coach_name)
        await ctx.respond("Team " + team_name + " created!", ephemeral=True)
    else:
        if str(user_id) in config["adminId"]:
            await teams.service.create(team_name, team_id, "no", "3", "BOT")
            await players.service.create_starting_eleven(team_id, coach_name)
            await ctx.respond("Team " + team_name + " created!", ephemeral=True)
        else:
            await ctx.respond("Sorry, you already have a team!", ephemeral=True)

async def view_team(ctx, user: discord.User):
    embed_team = await teams.service.getAll(str(user.id))
    await ctx.respond(embed=embed_team, ephemeral=False)
