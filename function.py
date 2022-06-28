import os
from riotwatcher import LolWatcher
import pandas as pd

TOKEN = os.environ['RTOKEN']
lol_watcher = LolWatcher(TOKEN)


def checkEnemy(name, region):
    if region == "euw":
        region = "euw1"
    elif region == "na":
        region = "na1"
    elif region == "tr":
        region = "tr1"
    else:
        print("You have entered a region that doesn't exist!")
    
    # Get summoner id
    summoner = lol_watcher.summoner.by_name(region, name)
    summoner_id = summoner['id']
    
    # Get all of the participants that are in the same game with the summoner
    spec = lol_watcher.spectator.by_summoner(region, summoner_id)
    participants = spec['participants']
    
    enemyteam_names = []
    enemyteam_ids = []
    enemyteam_puuids = []
    
    for i in participants:
        if i['summonerId'] == summoner_id:
            team = i['teamId']
    
    for i in participants:
        if i['teamId'] != team:
            enemyteam_names.append(i['summonerName'])
            enemyteam_ids.append(i['summonerId'])
    
    for i in enemyteam_ids:
        enemyteam_puuids.append(lol_watcher.summoner.by_id(region, i)['puuid'])
    
    match_history = []
    for i in enemyteam_puuids:
        match_history.append(lol_watcher.match.matchlist_by_puuid(region, i, count=10))
    
    players = {
        1: {'name': enemyteam_names[0], 'win': 0, 'lose': 0},
        2: {'name': enemyteam_names[1], 'win': 0, 'lose': 0},
        3: {'name': enemyteam_names[2], 'win': 0, 'lose': 0},
        4: {'name': enemyteam_names[3], 'win': 0, 'lose': 0},
        5: {'name': enemyteam_names[4], 'win': 0, 'lose': 0},
    }
    
    data = []
    
    for i in range(len(match_history)):
        for j in range(len(match_history[i])):
            data.extend(lol_watcher.match.by_id(region, match_history[i][j])['info']['participants'])
    
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

    df = pd.DataFrame(players).T
    return df












