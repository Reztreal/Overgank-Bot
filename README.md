# Overgank-Bot
#### Video Demo:  https://youtu.be/DNaqPhl_WV0
#### Description:
Overgank is a discord bot that uses a riot api library to fetch real in-game data.

RiotWatcher: https://github.com/pseudonym117/Riot-Watcher

Overgank Bot has two commands use and analyze. Use returns the way to use the bot properly. Analyze returns the win and lose numbers of the enemy team.
Because same summoner names can exist in different regions it is necessary to take region as input. 

def checkEnemy(name, region) is the main function that deals with the riot database and is the one that gathers all the data.
Using our earlier name and region input we ask for the summoner id using riot watcher. To use this bot the summoner must be in game or must be loading the game.
We spectate the current match the summoner in and take their names, ids and puuids which is a different kind of id Riot uses in their database.

Using the summoner puuids of the enemy team we create a list of lists called match_history. This list has all of the enemy team player's last 10 matches.
Then we create a dict called players so we can nicely represent our data.
    players = {
        1: {'name': enemyteam_names[0], 'win': 0, 'lose': 0},
        2: {'name': enemyteam_names[1], 'win': 0, 'lose': 0},
        3: {'name': enemyteam_names[2], 'win': 0, 'lose': 0},
        4: {'name': enemyteam_names[3], 'win': 0, 'lose': 0},
        5: {'name': enemyteam_names[4], 'win': 0, 'lose': 0},
    }

Now at this point we have to take a really big amount of data from riot and if you watched the video this part is why it takes so long.
We append every match data of the 50 matches we got earlier from going through the enemy team player's last 10 matches. I found that not saving this data to a list makes the program even slower.
    for i in range(len(match_history)):
        for j in range(len(match_history[i])):
            data.extend(lol_watcher.match.by_id(region, match_history[i][j])['info']['participants'])





In the last part of our program we go through the big chunk of data we got and record if the enemy player won or lost that specific game by incrementing either the lose or the win in our dictionary.
The process in the last 2 paragraphs used to be 3 nested for loops but that makes the program extremely slow so we have to consider the time complexity of our program.
In the final draft it is O(n^2) which is still pretty bad but I don't think there is any way to process data like this because of the nested nature of riot's api design and I'm not sure how else they could've implemented it.
    m = 0
    cout = 0
    for i in range(len(data)):
        if data[i]['puuid'] == enemyteam_puuids[m]:
            if data[i]['win']:
                players[m + 1]['win'] += 1
            else:
                players[m + 1]['lose'] += 1
        cout += 1
        if cout % 100 == 0:
            m += 1
