from random import choice

commentaries = {
    'matchStart': [
        "The match begins!",
        "The pitch looks perfect for today's game against **{HOME_TEAM}** and **{AWAY_TEAM}**",
        "Both **{HOME_TEAM}** and **{AWAY_TEAM}** are playing at a high level, we should be in for a thrilling game.",
        "The field conditions are less than ideal, let's see if that will have an impact on the game.",
        "Let's find out if **{AWAY_TEAM}** will be able to overcome **{HOME_TEAM}** in their fortress.",
        "The referee gets us underway in this match between **{HOME_TEAM}** & **{AWAY_TEAM}**.",
        "90 minutes plus added time are up and the referee blows his whistle.",
        "1 field, 2 teams, 22 players, 1 ball. Let's see what will happen now for this match between **{HOME_TEAM}** and **{AWAY_TEAM}**"
    ],
    'homeWin': [
        "At home, **{HOME_TEAM}** wins the game against *{AWAY_TEAM}*",
        "**{HOME_TEAM}** makes a great match and overcomes *{AWAY_TEAM}*",
        "Dominant performance by **{HOME_TEAM}**, well deserved the win and the 3 points.",
        "Mission accomplished for **{HOME_TEAM}** against *{AWAY_TEAM}* !"
    ],
    'awayWin': [
        "Away, **{AWAY_TEAM}** wins the game against *{HOME_TEAM}*",
        "**{AWAY_TEAM}** makes a great match and defeats *{HOME_TEAM}*",
        "It's full time and **{AWAY_TEAM}** have recorded a richly-deserved victory",
        "*{HOME_TEAM}* was surprised by **{AWAY_TEAM}** in this match !"
    ],
    'draw': [
        "What a game!\n**{HOME_TEAM}** and **{AWAY_TEAM}** were at the same level today.",
        "Nothing to separate the 2 sides today."
    ],
    'dominant': [
        "**{DOMINANT_TEAM}** is dominating the game!",
        "**{DOMINATED_TEAM}** don't see the light today!"
    ],
    'yellowCard': [
        "🟨 *{PLAYER_TEAM}*: It's a yellow card for **{PLAYER_NAME}**",
        "🟨 *{PLAYER_TEAM}*: That's going to be a yellow card for **{PLAYER_NAME}**!"
    ],
    'redCard': [
        "🟥 *{PLAYER_TEAM}*: It's a red card for **{PLAYER_NAME}**",
        "🟥 *{PLAYER_TEAM}*: **{PLAYER_NAME}** has prevented a clear goalscoring opportunity and has received his marching orders !"
    ],
    'shoot': [
        "**{PLAYER_NAME}** is in a good position and shoots...",
        "**{PLAYER_NAME}** goes for glory…",
        "**{PLAYER_NAME}** gets into a good shooting oppourtunity."
    ],
    'goal': [
        "⚽ What a goal for *{PLAYER_TEAM}* by **{PLAYER_NAME}** !",
        "⚽ GOOOOOOAAAAAL !! Beautiful shoot for *{PLAYER_TEAM}* by **{PLAYER_NAME}**",
        "⚽ Lovely cushioned header for **{PLAYER_NAME}** ! Ohhhhh, you beauty! What a hit son, what a hit",
        "⚽ It's in ! Clinical finishing by **{PLAYER_NAME}**",
        "⚽ **{PLAYER_NAME}** finds the net!",
        "⚽ An unbelievable strike by **{PLAYER_NAME}**, that one will be replayed over and over again!"
        "⚽ A brilliant goal! A brilliant goal! Remember the name **{PLAYER_NAME}**"
    ],
    'missedShot': [
        "Beautiful action for *{PLAYER_TEAM}* but **{PLAYER_NAME}** missed the shoot",
        "What was that ?! Poor shot by **{PLAYER_NAME}**",
        "Shot by **{PLAYER_NAME}** takes a wicked deflection and goes behind",
        "So close by **{PLAYER_NAME}** ! It's hit the post"
    ],
    'dangerousFoul': [
        "What a dangerous tackle from *{PLAYER_TEAM}* by **{PLAYER_NAME}**",
        "Tackle not mastered *{PLAYER_TEAM}* by **{PLAYER_NAME}**.. Fault !"
    ],
    'noCardAfterDangerousFoul': [
        "*{PLAYER_TEAM}*: No card for **{PLAYER_NAME}**",
        "The referee signals **{PLAYER_NAME}** to come closer... Last warning."
    ],
    'noAction': [
        "---"
    ]
}

def getCommentary(actionType, replacements = {}):
  return choice(commentaries[actionType]).format(**replacements)
