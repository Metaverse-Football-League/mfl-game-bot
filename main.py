import asyncio
import discord
from discord.ui import View, Button
from dotenv import load_dotenv
from random import randint, sample
import events
import leaderboards
import matchengine
import nfts
import players
import teams

### Prerequisites
# Discord2 Python library (py-cord)
# asyncio library
# names library to generate random names

### Files
## Players (DisplayName, OVR, Position, Owner, nationality, nft, rarity)
f_players = "players.csv"
## Teams
# Name, user_id, boolean(0 : bot, 1 : player, form)
f_teams = "teams.csv"
## Goal scorers (number, name, team)
f_goals = "goals.csv"
## Event (name, desc, status)
f_events = "events.csv"

load_dotenv(dotenv_path="config")
intents = discord.Intents.all()

### Set prefix
#bot = commands.Bot(command_prefix="!", intents=intents)
bot = discord.Bot()

### Discord configurations ###
gamechan = [983723647002882058, 989056372198998076]
adminid = "593086239024873483"

########################################################################################################
## START OF PROCESS ##
########################################################################################################

#### BOT IS READY ####
@bot.event
async def on_ready():
    print("Bot Ready")

#### CREATE TEAM ####
@bot.command(name='create', description='The first step to enter into the game...')
async def create(ctx, name):
    # Usage : !create Team_Name
    if ctx.channel.id in gamechan:
        teamname = name
        with open(f_teams, "r+") as tfile:
            user = ctx.interaction.user
            user_id = str(user.id)
            if user.id > 1000000:
                username = user.name
            else:
                username = "BOT"
            team_id = user_id
            if user_id in tfile.read():
                if user_id == adminid:
                    team_id = str(randint(1, 999999))
                    tfile.write(teamname + "," + team_id + ",no,3,BOT,\n")
                    await players.create(team_id, username)
                    await ctx.respond("Team " + teamname + " created !", ephemeral=True)
                else:
                    await ctx.respond("Sorry, you already have a team !", ephemeral=True)
            else:
                tfile.write(teamname + "," + team_id + ",yes,3,"+username+"\n")
                await players.create(team_id, username)
                await ctx.respond("Team " + teamname + " created !", ephemeral=True)


@bot.command(name='view')
async def change(ctx, user: discord.User):
    if ctx.channel.id in gamechan:
        embedteam = await teams.get_All(str(user.id))
        await ctx.respond(embed=embedteam, ephemeral=False)


@bot.command(name='match', description="Start a match !")
async def match(ctx, user1: discord.User, user2: discord.User):
    if ctx.channel.id in gamechan:
        events = "no"
        match = await matchengine.play(str(user1.id), str(user2.id), events)
        view = View()
        default_color = 0x00ff00
        embedmenu = discord.Embed(
            title='Discord Football Game', color=default_color)

        showmenu = await ctx.respond("\u200b", view=view, embed=embedmenu, ephemeral=False)

        for x in match:
            #await showmenu.edit(view=view, embed=x)
            await showmenu.edit_original_message(view=view, embed=x)
            await asyncio.sleep(1)


#### Menu display
@bot.command(name='game', description='Access to the menu, build your team and compete...')
async def game(ctx):
    if ctx.channel.id in gamechan:
        user_id = str(ctx.interaction.user.id)
        user_name = str(ctx.interaction.user)
        default_color = 0x00ff00
        embedmenu = discord.Embed(
            title='Discord Football Game', color=default_color)
        embedmenu.add_field(name="Hello", value="Want play ?", inline=True)

        button_play = Button(label="Play", style=discord.ButtonStyle.green, custom_id="play", emoji="⚽")
        button_scout = Button(label="Scout", style=discord.ButtonStyle.green, custom_id="scout", emoji="👨")
        button_nfts = Button(label="NFT", style=discord.ButtonStyle.blurple, row=2, custom_id="nfts", emoji="🎉")
        button_team = Button(label="Team", style=discord.ButtonStyle.green, custom_id="team", emoji="👥")
        button_recruit = Button(label="Recruit", style=discord.ButtonStyle.green, custom_id="recruit", emoji="✅")
        button_letleave = Button(label="Return", style=discord.ButtonStyle.grey, custom_id="letleave", emoji="❌")
        button_finishmatch = Button(label="Skip", style=discord.ButtonStyle.blurple, custom_id="finishmatch")
        button_leaderboard = Button(label="Leaderboard", style=discord.ButtonStyle.grey, row=1, custom_id="leaderboard",
                                    emoji="🏆")
        button_events = Button(label="Events", style=discord.ButtonStyle.blurple, row=1, custom_id="events", emoji="⭐")

        viewdefault = View()
        viewdefault.add_item(button_team)
        viewdefault.add_item(button_scout)
        viewdefault.add_item(button_play)
        viewdefault.add_item(button_events)
        viewdefault.add_item(button_leaderboard)
        viewdefault.add_item(button_nfts)

        viewmatch = View()
        viewmatch.add_item(button_finishmatch)
        viewmatch.add_item(button_team)

        skip = 0

        async def button_play_callback(interaction):
            if str(interaction.user) == user_name:
                embedteam, teamlist = await teams.find(user_id)
                eventlist = await events.get("vs")

                viewopponents = View()
                i = 1

                if eventlist[0] != "":
                    button_ev1 = None
                    button_ev2 = None
                    button_ev3 = None
                    button_ev4 = None
                    button_ev5 = None

                    for event in eventlist:
                        code = event.code
                        name = event.name
                        desc = event.desc
                        status = event.status
                        kind = event.kind
                        opponent = event.opponent

                        if i == 1:
                            button_ev1 = Button(label=name, style=discord.ButtonStyle.blurple,
                                                    row=1, custom_id=code+","+opponent)
                            viewopponents.add_item(button_ev1)
                        elif i == 2:
                            button_ev2 = Button(label=name, style=discord.ButtonStyle.blurple,
                                                    row=1, custom_id=code+","+opponent)
                            viewopponents.add_item(button_ev2)
                        elif i == 3:
                            button_ev3 = Button(label=name, style=discord.ButtonStyle.blurple,
                                                    row=1, custom_id=code+","+opponent)
                            viewopponents.add_item(button_ev3)
                        elif i == 4:
                            button_ev4 = Button(label=name, style=discord.ButtonStyle.blurple,
                                                    row=1, custom_id=code+","+opponent)
                            viewopponents.add_item(button_ev4)
                        elif i == 5:
                            button_ev5 = Button(label=name, style=discord.ButtonStyle.blurple,
                                                    row=1, custom_id=code+","+opponent)
                            viewopponents.add_item(button_ev5)
                        i += 1



                id_random = str(teamlist[2].split(",")[1])
                button_random = Button(label="vs Random", style=discord.ButtonStyle.grey, custom_id=id_random,
                                       emoji="⚽")
                viewopponents.add_item(button_random)

                i = 1
                for x in teamlist:
                    name = x.split(",")[0]
                    vs_id = x.split(",")[1]
                    if i == 1:
                        button_vs1 = Button(label=name, style=discord.ButtonStyle.green, custom_id=str(vs_id))
                        viewopponents.add_item(button_vs1)
                    elif i == 2:
                        button_vs2 = Button(label=name, style=discord.ButtonStyle.green, custom_id=str(vs_id))
                        viewopponents.add_item(button_vs2)
                    i += 1

                viewopponents.add_item(button_team)

                await showmenu.edit_original_message(view=viewopponents, embed=embedteam)
                await interaction.response.defer()

                async def button_vs_callback(interaction):
                    if str(interaction.user) == user_name:
                        global skip
                        skip = 0

                        viewmatch = View()
                        viewmatch.add_item(button_finishmatch)
                        viewmatch.add_item(button_team)

                        vs = interaction.data['custom_id']
                        if "event_" in vs:
                            events = vs.split(",")[0]
                            vs = vs.split(",")[1]
                        else:
                            events = "no"

                        embedlist = await matchengine.play(user_id, vs, events)

                        async def button_finishmatch_callback(interaction):
                            global skip

                            if str(interaction.user) == user_name:
                                skip = 1
                                await showmenu.edit_original_message(view=viewmatch, embed=embedlist[-1])
                                await interaction.response.defer()

                        for x in embedlist:

                            button_finishmatch.callback = button_finishmatch_callback
                            if skip == 1:
                                break

                            await showmenu.edit_original_message(view=viewmatch, embed=x)
                            await asyncio.sleep(1)

                            try:
                                await interaction.response.defer()
                            except discord.InteractionResponded:
                                continue

                button_random.callback = button_vs_callback
                button_vs1.callback = button_vs_callback
                button_vs2.callback = button_vs_callback
                if button_ev1:
                    button_ev1.callback = button_vs_callback
                if button_ev2:
                    button_ev2.callback = button_vs_callback
                if button_ev3:
                    button_ev3.callback = button_vs_callback
                if button_ev4:
                    button_ev4.callback = button_vs_callback
                if button_ev5:
                    button_ev5.callback = button_vs_callback

        async def button_team_callback(interaction):
            if str(interaction.user) == user_name:
                embedteam = await teams.get_All(user_id)

                view = View()
                view.add_item(button_team)
                view.add_item(button_scout)
                view.add_item(button_play)
                view.add_item(button_events)
                view.add_item(button_leaderboard)
                view.add_item(button_nfts)

                await showmenu.edit_original_message(view=view, embed=embedteam)
                await interaction.response.defer()

        async def button_nfts_callback(interaction):
            if str(interaction.user) == user_name:
                global indice
                indice = 0

                await interaction.response.defer()

                playerslist = await nfts.get(user_id, indice)

                async def nftembed(playerslist, indice):
                    default_color = 0xffff00
                    embednfts = discord.Embed(
                        title="Your NFTS", description="Below your squad", color=default_color)
                    description = ""
                    buttons = []
                    b1 = None
                    b2 = None
                    b3 = None
                    b4 = None
                    b5 = None
                    i = 0
                    for x in playerslist[indice]:
                        nation = x.split(",")[0]
                        positions = x.split(",")[1]
                        ovr = x.split(",")[2]
                        displayName = x.split(",")[3]
                        rarity = x.split(",")[4]

                        if rarity == "common":
                            rarity_flag = "⚪"
                        elif rarity == "uncommon":
                            rarity_flag = "🟢"
                        elif rarity == "rare":
                            rarity_flag = "🔵"
                        elif rarity == "legend":
                            rarity_flag = "🟣"

                        if len(positions) == 3:
                            description = description + ":flag_" + nation + ":`" + positions + " " + str(
                                ovr) + "`" + rarity_flag + " *" + displayName + "*\n"
                        else:
                            description = description + ":flag_" + nation + ":`" + positions + "  " + str(
                                ovr) + "`" + rarity_flag + " *" + displayName + "*\n"

                        if i == 0:
                            b1 = Button(label=displayName, style=discord.ButtonStyle.blurple, row=1, custom_id="Player "+str(i))
                            buttons.append(b1)
                        elif i == 1:
                            b2 = Button(label=displayName, style=discord.ButtonStyle.blurple, row=1, custom_id="Player "+str(i))
                            buttons.append(b2)
                        elif i == 2:
                            b3 = Button(label=displayName, style=discord.ButtonStyle.blurple, row=1, custom_id="Player "+str(i))
                            buttons.append(b3)
                        elif i == 3:
                            b4 = Button(label=displayName, style=discord.ButtonStyle.blurple, row=1, custom_id="Player "+str(i))
                            buttons.append(b4)
                        elif i == 4:
                            b5 = Button(label=displayName, style=discord.ButtonStyle.blurple, row=1, custom_id="Player "+str(i))
                            buttons.append(b5)
                        i += 1

                    embednfts.add_field(name="Players", value=description)

                    viewnfts = View()
                    viewnfts.add_item(button_previous)
                    viewnfts.add_item(button_next)
                    viewnfts.add_item(button_team)

                    async def button_scoutnft_callback(interaction):
                        if str(interaction.user) == user_name:
                            viewscout = View()
                            viewscout.add_item(button_team)
                            viewscout.add_item(button_recruit)
                            viewscout.add_item(button_letleave)

                            select = int(interaction.data['custom_id'].split(" ")[1])
                            player = playerslist[indice][select]
                            nat = player.split(",")[0]
                            pos = player.split(",")[1]
                            ovr = player.split(",")[2]
                            name = player.split(",")[3]
                            rarity = player.split(",")[4]

                            alreadyinTeam = await players.check(user_id, name)

                            if alreadyinTeam == True:

                                default_color = 0xffff00
                                embedscout = discord.Embed(
                                    title="Error", description="This player is already in your team", color=default_color)

                                view = View()
                                view.add_item(button_team)
                                view.add_item(button_scout)
                                view.add_item(button_play)
                                view.add_item(button_events)
                                view.add_item(button_leaderboard)
                                view.add_item(button_nfts)

                                await showmenu.edit_original_message(view=view, embed=embedscout)
                                await interaction.response.defer()

                            else:
                                embedscout = await nfts.scout(user_id, name, ovr, pos, nat, rarity)

                                await showmenu.edit_original_message(view=viewscout, embed=embedscout)
                                await interaction.response.defer()

                    if b1:
                        b1.callback = button_scoutnft_callback
                    if b2:
                        b2.callback = button_scoutnft_callback
                    if b3:
                        b3.callback = button_scoutnft_callback
                    if b4:
                        b4.callback = button_scoutnft_callback
                    if b5:
                        b5.callback = button_scoutnft_callback

                    for x in buttons:
                        viewnfts.add_item(x)

                    return embednfts, viewnfts

                async def button_move_callback(interaction):
                    global indice
                    if str(interaction.user) == user_name:
                        page = interaction.data['custom_id']
                        if page == "next":
                            indice += 1
                        elif page == "prev":
                            indice -= 1

                        embednfts, viewnfts = await nftembed(playerslist, indice)


                        await showmenu.edit_original_message(view=viewnfts, embed=embednfts)
                        await interaction.response.defer()

                button_previous = Button(style=discord.ButtonStyle.blurple, custom_id="prev", emoji="◀")
                button_next = Button(style=discord.ButtonStyle.blurple, custom_id="next", emoji="▶")
                button_next.callback = button_move_callback
                button_previous.callback = button_move_callback

                embednfts, viewnfts = await nftembed(playerslist, indice)

                await showmenu.edit_original_message(view=viewnfts, embed=embednfts)
                #await interaction.response.defer()

        async def button_scout_callback(interaction):
            if str(interaction.user) == user_name:
                viewscout = View()
                viewscout.add_item(button_team)
                viewscout.add_item(button_recruit)
                viewscout.add_item(button_letleave)
                embedplayer = await players.scout(user_id)
                await showmenu.edit_original_message(view=viewscout, embed=embedplayer)
                await interaction.response.defer()

        async def button_leaderboard_callback(interaction):
            if str(interaction.user) == user_name:

                viewlead = View()
                viewlead.add_item(button_team)
                viewlead.add_item(button_scout)
                viewlead.add_item(button_play)

                embedlead = await leaderboards.get(user_id)
                eventlist = await events.get("vs")
                i = 1

                button_global = Button(label="Global", style=discord.ButtonStyle.blurple,
                                        row=1, custom_id="goals")
                viewlead.add_item(button_global)

                if eventlist[0] != "":
                    button_ev1 = None
                    button_ev2 = None
                    button_ev3 = None
                    button_ev4 = None
                    button_ev5 = None

                    for event in eventlist:
                        code = event.code
                        name = event.name
                        desc = event.desc
                        status = event.status
                        kind = event.kind
                        opponent = event.opponent

                        if i == 1:
                            button_ev1 = Button(label=name, style=discord.ButtonStyle.blurple,
                                                    row=2, custom_id=code+","+opponent)
                            viewlead.add_item(button_ev1)
                        elif i == 2:
                            button_ev2 = Button(label=name, style=discord.ButtonStyle.blurple,
                                                    row=2, custom_id=code+","+opponent)
                            viewlead.add_item(button_ev2)
                        elif i == 3:
                            button_ev3 = Button(label=name, style=discord.ButtonStyle.blurple,
                                                    row=2, custom_id=code+","+opponent)
                            viewlead.add_item(button_ev3)
                        elif i == 4:
                            button_ev4 = Button(label=name, style=discord.ButtonStyle.blurple,
                                                    row=2, custom_id=code+","+opponent)
                            viewlead.add_item(button_ev4)
                        elif i == 5:
                            button_ev5 = Button(label=name, style=discord.ButtonStyle.blurple,
                                                    row=2, custom_id=code+","+opponent)
                            viewlead.add_item(button_ev5)
                        i += 1

                async def button_leads_callback(interaction):
                    event = interaction.data['custom_id'].split(",")[0]

                    embedlead = await leaderboards.get(event)

                    await showmenu.edit_original_message(view=viewlead, embed=embedlead)
                    await interaction.response.defer()


                button_global.callback = button_leads_callback
                if button_ev1:
                    button_ev1.callback = button_leads_callback
                if button_ev2:
                    button_ev2.callback = button_leads_callback
                if button_ev3:
                    button_ev3.callback = button_leads_callback
                if button_ev4:
                    button_ev4.callback = button_leads_callback
                if button_ev5:
                    button_ev5.callback = button_leads_callback

                await showmenu.edit_original_message(view=viewlead, embed=embedlead)
                await interaction.response.defer()

        async def button_events_callback(interaction):
            if str(interaction.user) == user_name:
                eventlist = await events.get("all")

                default_color = 0x00ff00
                embedevent = discord.Embed(
                    title="Events", description="Below the list of current events", color=default_color)

                for event in eventlist:
                    code = event.code
                    name = event.name
                    desc = event.desc
                    status = event.status
                    kind = event.kind

                    embedevent.add_field(name=name, value=desc)

                await showmenu.edit_original_message(view=view, embed=embedevent)
                await interaction.response.defer()

        async def button_recruit_callback(interaction):
            if str(interaction.user) == user_name:
                playerscheck = interaction.message.embeds[0].fields
                playersinfos = playerscheck[0].value.split(" ")
                nat = playersinfos[0].split("`")[0].split("_")[1].replace(":", "")
                num = playersinfos[0].split("`")[1]

                pos = playersinfos[2]
                ovr = playersinfos[3].replace("`", "")
                name = playersinfos[5] + " " + playersinfos[6]

                name = name.replace("*", "")
                await players.recruit(user_id, num, name, ovr, pos, nat)
                embedteam = await teams.get_All(user_id)

                view = View()
                view.add_item(button_team)
                view.add_item(button_scout)
                view.add_item(button_play)
                view.add_item(button_events)
                view.add_item(button_leaderboard)
                view.add_item(button_nfts)

                await showmenu.edit_original_message(view=view, embed=embedteam)
                await interaction.response.defer()

        async def button_letleave_callback(interaction):
            if str(interaction.user) == user_name:

                view = View()
                view.add_item(button_team)
                view.add_item(button_scout)
                view.add_item(button_play)
                view.add_item(button_events)
                view.add_item(button_leaderboard)
                view.add_item(button_nfts)

                await showmenu.edit_original_message(view=view, embed=embedmenu)
                await interaction.response.defer()

        button_play.callback = button_play_callback
        button_events.callback = button_events_callback
        button_leaderboard.callback = button_leaderboard_callback
        button_team.callback = button_team_callback
        button_scout.callback = button_scout_callback
        button_recruit.callback = button_recruit_callback
        button_letleave.callback = button_letleave_callback
        button_nfts.callback = button_nfts_callback

        view = viewdefault

        showmenu = await ctx.respond("\u200b", view=view, embed=embedmenu, ephemeral=True)


#### BOT TOKEN ########################
with open('token.txt', 'r') as f:
    token = f.readline()
bot.run(token)
