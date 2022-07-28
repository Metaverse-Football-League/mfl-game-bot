from random import choice

commentaries = {
    'matchStart': [
        "The match begins!",
        "The pitch looks perfect for today's game against *{HOME_TEAM}* and *{AWAY_TEAM}*",
        "Both *{HOME_TEAM}* and *{AWAY_TEAM}* are playing at a high level, we should be in for a thrilling game.",
        "The field conditions are less than ideal, let's see if that will have an impact on the game.",
        "Let's find out if *{AWAY_TEAM}* will be able to overcome *{HOME_TEAM}* in their fortress.",
        "The referee gets us underway in this match between *{HOME_TEAM}* & *{AWAY_TEAM}*.",
        "90 minutes plus added time are up and the referee blows his whistle.",
        "1 field, 2 teams, 22 players, 1 ball. Let's see what will happen now for this match between *{HOME_TEAM}* and *{AWAY_TEAM}*",
        "A lovely evening here as *{HOME_TEAM}* look to secure the win in front of their home crowd. *{START_PLAYER_NAME}* kicks things off and we are underway!",
        "*{AWAY_TEAM}* and *{HOME_TEAM}* are ready to battle it out in what should be an entertaining contest. *{START_PLAYER_NAME}* gets us underway.",
        "KICK OFF! The referee signals the start of the match and *{START_PLAYER_NAME}* get us underway."
    ],
    'homeWin': [
        "At home, *{HOME_TEAM}* wins the game against *{AWAY_TEAM}*",
        "**{HOME_TEAM}** makes a great match and overcomes *{AWAY_TEAM}*",
        "Dominant performance by *{HOME_TEAM}*, well deserved the win and the 3 points.",
        "Mission accomplished for *{HOME_TEAM}* against *{AWAY_TEAM}* !",
        "Full time! It's all over and *{HOME_TEAM}* fans are on their feet to applaud a very good performance by the hosts.",
        "FULL TIME! That's all the action for today, as *{HOME_TEAM}* defeat *{AWAY_TEAM}* in an action-packed encounter.",
        "FULL TIME! *{HOME_TEAM}* players celebrate their well-deserved victory over the visitors!",
        "Final whistle! *{HOME_TEAM}* prevail over *{AWAY_TEAM}* on their home turf."
    ],
    'awayWin': [
        "Away, *{AWAY_TEAM}* wins the game against *{HOME_TEAM}*",
        "**{AWAY_TEAM}** makes a great match and defeats *{HOME_TEAM}*",
        "It's full time and *{AWAY_TEAM}* have recorded a richly-deserved victory",
        "**{HOME_TEAM}** was surprised by *{AWAY_TEAM}* in this match !",
        "The referee blows the final whistle. A disappointing performance by the hosts sees *{AWAY_TEAM}* take this one!",
        "Final whistle! *{AWAY_TEAM}* comes out on top while the home side comes away empty-handed.",
        "Full Time! *{AWAY_TEAM}* players celebrate their well-deserved victory over the hosts today!",
        "Full time! That's all the action for today, as *{AWAY_TEAM}* defeat *{HOME_TEAM}* in an action-packed encounter."
    ],
    'draw': [
        "What a game!\n**{HOME_TEAM}** and *{AWAY_TEAM}* were at the same level today.",
        "Nothing to separate the 2 sides today.",
        "DRAW! No winners today as this hard-fought battle comes to a close.",
        "It's a draw! *{HOME_TEAM}* manage to defend home turf against a tough *{AWAY_TEAM}* side."
    ],
    'dominant': [
        "**{DOMINANT_TEAM}** is dominating the game!",
        "**{DOMINATED_TEAM}** don't see the light today!",
        "**{DOMINANT_TEAM}** have been absolutely dominant so far in this contest.",
        "**{DOMINANT_TEAM}** have taken control of this match. Can *{DOMINATED_TEAM}* hold on?",
        "This is becoming a one-sided affair with *{DOMINANT_TEAM}* now largely in control of the ball.",
        "**{DOMINANT_TEAM}** seem to have upped their intensity and it's unsettled *{DOMINATED_TEAM}*.",
        "**{DOMINATED_TEAM}** must be hoping *{DOMINANT_TEAM}* take their foot off the gas. They're struggling!",
        "**{DOMINANT_TEAM}** are toying with their opponents at this point."
    ],
    'yellowCard': [
        "🟨 *{PLAYER_TEAM}*: It's a yellow card for *{PLAYER_NAME}*",
        "🟨 *{PLAYER_TEAM}*: That's going to be a yellow card for *{PLAYER_NAME}*!",
        "🟨 YELLOW CARD! *{PLAYER_NAME}* is booked for *{PLAYER_TEAM}*."
    ],
    'redCard': [
        "🟥 *{PLAYER_TEAM}*: It's a red card for *{PLAYER_NAME}*",
        "🟥 *{PLAYER_TEAM}*: *{PLAYER_NAME}* has prevented a clear goalscoring opportunity and has received his marching orders !",
        "🟥 RED CARD! *{PLAYER_NAME}* is sent off! *{PLAYER_TEAM}* will have to do without him."
    ],
    'shoot': [
        "**{PLAYER_NAME}** is in a good position and shoots...",
        "**{PLAYER_NAME}** goes for glory…",
        "**{PLAYER_NAME}** gets into a good shooting oppourtunity.",
        "**{PLAYER_NAME}** collects a lovely ball and looks up"
        "**{PLAYER_TEAM}** gain possession in midfield and *{PLAYER_NAME}* gets in behind",
        "**{PLAYER_TEAM}** launch a blistering counter-attack after winning the ball back! Three on two!",
        "Brilliant effort from the *{PLAYER_TEAM}* midfield as the ball quickly makes its way forward",
        "It looks like *{PLAYER_NAME}* is going to have a crack at it!",
        "**{PLAYER_NAME}** gets in behind and is through on goal…",
        "**{PLAYER_NAME}** tries a first-time volley from the cross…",
        "**{PLAYER_NAME}** finds some space and lets it fly from long range…",
        "**{PLAYER_NAME}** attempts an overhead kick…",
        "**{PLAYER_NAME}** unleashes a powerful outside-of-the-boot half-volley…",
        "**{PLAYER_NAME}** beats the offside trap and tries to chip it over the goalie…",
        "**{PLAYER_NAME}** tries to curl one into the top corner from the edge of the box…",
        "**{PLAYER_NAME}** loses his man and elevates for the powerful near-post header…",
        "**{PLAYER_NAME}** curls a dipping shot low towards the far post…"
    ],
    'goal': [
        "⚽ What a goal for *{PLAYER_TEAM}* by *{PLAYER_NAME}* !",
        "⚽ GOOOOOOAAAAAL !! Beautiful shoot for *{PLAYER_TEAM}* by *{PLAYER_NAME}*",
        "⚽ Lovely cushioned header for *{PLAYER_NAME}* ! Ohhhhh, you beauty! What a hit son, what a hit",
        "⚽ It's in ! Clinical finishing by *{PLAYER_NAME}*",
        "⚽ *{PLAYER_NAME}* finds the net!",
        "⚽ An unbelievable strike by *{PLAYER_NAME}*, that one will be replayed over and over again!"
        "⚽ A brilliant goal! A brilliant goal! Remember the name *{PLAYER_NAME}*",
        "⚽ GOAAAAL! *{PLAYER_NAME}* timed his run perfectly! He beats the offside trap and chips it over the goalie!",
        "⚽ OH MY WORD! What a strike from *{PLAYER_NAME}*! He curls that one right into the top corner!",
        "⚽ GOAL! It's in! A clinical finish into the bottom corner from *{PLAYER_NAME}*, he left the goalkeeper no chance!",
        "⚽ *{PLAYER_NAME}*! He slots it through the keeper's legs!",
        "⚽ GOAL! *{PLAYER_NAME}* loses his man and smashes a powerful header into the back of the net!",
        "⚽ GOAL! Out of nothing! A wonderful touch and hit by *{PLAYER_NAME}*! Brilliant!",
        "⚽ *{PLAYER_NAME}*! HOW ABOUT THAT! He unleashes a powerful outside-of-the-boot half-volley into the top corner!",
        "⚽ GOALLL! A stunner from *{PLAYER_NAME}* who fires an absolute rocket from long range!",
        "⚽ GOAL! His teammate's shot is deflected, but *{PLAYER_NAME}* is positioned perfectly and just has to tap it in!",
        "⚽ OH MY WORD! What a strike from *{PLAYER_NAME}*! GOAAAL!",
        "⚽ GOAL! It's in! A clinical finish from *{PLAYER_NAME}*, he left the goalkeeper no chance!",
        "⚽ *{PLAYER_NAME}* scores! A wonderful move and finish!",
        "⚽ GOAL! *{PLAYER_NAME}* puts it away! He rushes to the corner flag in celebration!",
        "⚽ GOAL! Out of nothing! A wonderful touch and hit by *{PLAYER_NAME}*! Brilliant!",
        "⚽ *{PLAYER_NAME}*! HOW ABOUT THAT! A magnificent goal from the man of the moment!",
        "⚽ GOALLL! A stunner from *{PLAYER_NAME}*! He tells the keeper to go pick that one out of the net!",
        "⚽ GOAL! It doesn't get much better than that! A truly incredible goal from *{PLAYER_NAME}*!"
    ],
    'missedShot': [
        "Beautiful action for *{PLAYER_TEAM}* but *{PLAYER_NAME}* missed the shoot",
        "What was that ?! Poor shot by *{PLAYER_NAME}*",
        "Shot by *{PLAYER_NAME}* takes a wicked deflection and goes behind",
        "So close by *{PLAYER_NAME}* ! It's hit the post",
        "**{PLAYER_NAME}** is through and just has the keeper to beat. He completely misses the target!",
        "The goalkeeper deflects *{PLAYER_NAME}*'s volley onto the post! Brilliant save!",
        "**{PLAYER_NAME}** fires a shot inside the box but the defender slides in to block it!",
        "Close! *{PLAYER_NAME}* elevates over two defenders at the far post but his header is wide. What a chance!",
        "**{PLAYER_NAME}** curls a dipping shot low towards the near post! It's tipped wide by the goalkeeper.",
        "**{PLAYER_NAME}** lets if fly from 30 yards, but his shot is comfortably saved by the goalie.",
        "**{PLAYER_NAME}** gets in behind and into the box but his shot ends up in the side netting.",
        "**{PLAYER_NAME}** tries an acrobatic move… that was ambitious. Goal kick.",
        "**{PLAYER_NAME}** completely misses the target.",
        "The goalkeeper deflects *{PLAYER_NAME}*'s shot onto the post! Brilliant save!",
        "The defender slides in to block *{PLAYER_NAME}*'s shot! An amazing defensive play!",
        "Close! The keeper has his crossbar to thank after this effort from *{PLAYER_NAME}*. What a chance!",
        "It's tipped wide by the goalkeeper. A great effort from *{PLAYER_NAME}*, but an even better save!",
        "**{PLAYER_NAME}**'s shot is comfortably saved by the goalie.",
        "**{PLAYER_NAME}**'s shot ends up in the side netting.",
        "Well, that was certainly ambitious from *{PLAYER_NAME}*. Goal kick.",
        "**{PLAYER_NAME}** blazes it over the bar."
    ],
    'dangerousFoul': [
        "What a dangerous tackle from *{PLAYER_TEAM}* by *{PLAYER_NAME}*",
        "Tackle not mastered *{PLAYER_TEAM}* by *{PLAYER_NAME}*.. Foul !",
        "FOUL! *{PLAYER_NAME}* brings the striker down. He had a clear run at goal!",
        "FOUL! Play is stopped after *{PLAYER_NAME}* pulls an opponent's shirt.",
        "FOUL! The referee blows his whistle after an awfully late challenge from *{PLAYER_NAME}*.",
        "FOUL! That was a reckless challenge from *{PLAYER_NAME}*, who slid right from behind! Ouch."
    ],
    'noCardAfterDangerousFoul': [
        "*{PLAYER_TEAM}*: No card for *{PLAYER_NAME}*",
        "The referee signals *{PLAYER_NAME}* to come closer... Last warning.",
        "The referee asks *{PLAYER_NAME}* over for a chat. Final warning.",
        "**{PLAYER_NAME}** escapes without a booking."
    ],
    'noAction': [
        "---"
    ]
}

def getCommentary(actionType, replacements = {}):
  return choice(commentaries[actionType]).format(**replacements)
