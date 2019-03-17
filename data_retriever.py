import requests
import csv
import json

player_teammates_2018_stats = {}

PREVIOUS_SEASONS = {"2017-18": {}, "2016-17": {}}
player_stats_dict = {"2018-19": player_teammates_2018_stats}
player_stats_dict.update(PREVIOUS_SEASONS)


def write_as_json(player_stats_season_dict):
    filename_format = './json_data/stats_%s.json'
    for season in player_stats_season_dict:
        filename = filename_format % season
        with open(filename, 'w') as jsonFile:
            json.dump(player_stats_season_dict[season], jsonFile, indent=4, sort_keys=True)


def create_dict_from_csv(season, player_name, player_id):
    players_hist_stats = requests.get(GITHUB_STATS_BASE_URL % (season, playerName)).content.decode('utf-8')
    dict_after_csv = csv.DictReader(players_hist_stats.splitlines(), delimiter=',')
    player_stats_dict[season][player_id] = {NAME: player_name, STATS: list(dict_after_csv)}


BASE_URL = "https://fantasy.premierleague.com/drf/%s"
STATIC = BASE_URL % "/bootstrap-static"
FIXTURES = BASE_URL % "/fixtures"
PLAYER = BASE_URL % "/element-summary/"
NAME = "name"
STATS = "stats"

GITHUB_STATS_BASE_URL = "https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/%s/players/%s/gw.csv?datatype=csv"
ID_ELEMENT = 'id'

playerToRunId = 253
playerToRunTeamId = -1
print("Getting all PL players!")

# with open('static.json', encoding='utf-8') as data_file:
#     players = json.load(data_file)['elements']
players = requests.get(STATIC).json()['elements']
print("Got ", len(players), " players!")

for player in players:
    playerId = player[ID_ELEMENT]

    if playerId == playerToRunId:
        playerToRunTeamId = player['team_code']
        print("Player ", playerToRunId, " belongs to team ", playerToRunTeamId)
        break

if playerToRunTeamId != -1:
    for player in players:
        if playerToRunTeamId == player['team_code']:
            playerId = player[ID_ELEMENT]
            playerName = player['first_name'] + '_' + player['second_name']
            params = {
                "id": playerId
            }
            print("Fetching player with id: ", playerId, ", name: ", playerName)
            # with open('players.json', encoding='utf-8') as data_file:
            #     playerTeamMates[playerId] = json.load(data_file)
            player_stats = requests.get(PLAYER + str(playerId), params).json()['history']
            player_teammates_2018_stats[playerId] = {NAME: playerName, STATS: player_stats}

            for previous_season in PREVIOUS_SEASONS:
                create_dict_from_csv(previous_season, playerName, playerId)
else:
    print("Player ", playerToRunId, " does not belong to any team!")

write_as_json(player_stats_dict)
