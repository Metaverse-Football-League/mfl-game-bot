from random import choice

commentaries = {
    'matchStart': [
        "The match begins!",
        "The pitch looks perfect for today's game against **{HOME_TEAM}** and **{AWAY_TEAM}**",
        "Both **{HOME_TEAM}** and **{AWAY_TEAM}** are playing at a high level, we should be in for a thrilling game.",
        "The field conditions are less than ideal, let's see if that will have an impact on the game.",
        "Let's find out if **{AWAY_TEAM}** will be able to overcome **{HOME_TEAM}** in their fortress.",
        "1 field, 2 teams, 22 players, 1 ball. Let's see what will happen now for this match between **{HOME_TEAM}** and **{AWAY_TEAM}**"
    ],
    'homeWin': [
        "At home, **{HOME_TEAM}** wins the game against *{AWAY_TEAM}*",
        "**{HOME_TEAM}** makes a great match and overcomes *{AWAY_TEAM}*",
        "Mission accomplished for **{HOME_TEAM}** against *{AWAY_TEAM}* !"
    ],
    'awayWin': [
        "Away, **{AWAY_TEAM}** wins the game against *{HOME_TEAM}*",
        "**{AWAY_TEAM}** makes a great match and overcomes *{HOME_TEAM}*"
        "*{HOME_TEAM}* was surprised by **{AWAY_TEAM}** in this match !"
    ],
    'draw': [
        "What a game!\n**{HOME_TEAM}** and **{AWAY_TEAM}** were at the same level today."
    ],
    'dominant': [
        "**{DOMINANT_TEAM}** is dominating the game!",
        "**{DOMINATED_TEAM}** don't see the light today!"
    ],
    'yellowCard': [
        "🟨 *{PLAYER_TEAM}*: It's a yellow card for **{PLAYER_NAME}**",
    ],
    'redCard': [
        "🟥 *{PLAYER_TEAM}*: It's a red card for **{PLAYER_NAME}**",
    ],
    'shoot': [
        "**{PLAYER_NAME}** is in a good position and shoot...",
    ],
    'goal': [
        "⚽ What a goal for *{PLAYER_TEAM}* by **{PLAYER_NAME}** !",
        "⚽ GOOOOOOAAAAAL !! Beautiful shoot for *{PLAYER_TEAM}* by **{PLAYER_NAME}**",
        "⚽ Lovely cushing header for **{PLAYER_NAME}** ! Ohhhhh, you beauty! What a hit son, what a hit",
        "⚽ It's in ! Clinical finishing by **{PLAYER_NAME}**",
        "⚽ A brilliant goal! A brilliant goal! Remember the name **{PLAYER_NAME}**"
    ],
    'missedShot': [
        "Beautiful action for *{PLAYER_TEAM}* but **{PLAYER_NAME}** missed the shoot",
        "What was that ?! Poor shoot by **{PLAYER_NAME}**",
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
