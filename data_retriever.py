import requests
import json

BASE_URL = "https://fantasy.premierleague.com/drf"
STATIC = BASE_URL + "/bootstrap-static"
FIXTURES = BASE_URL + "/fixtures"
PLAYER = BASE_URL + "/element-summary/"
NAME = "name"
STATS = "stats"

ID_ELEMENT = 'id'

playerToRunId = 253
playerToRunTeamId = -1
playerTeamMates = {}

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
            playerName = player['first_name'] + ' ' + player['second_name']
            params = {
                "id": playerId
            }
            print("Fetching player with id: ", playerId, ", name: ", playerName)
        # with open('players.json', encoding='utf-8') as data_file:
        #     playerTeamMates[playerId] = json.load(data_file)
            player_stats = requests.get(PLAYER + str(playerId), params).json()['history']
            playerTeamMates[playerId] = {NAME: playerName, STATS: player_stats}
else:
    print("Player ", playerToRunId, " does not belong to any team!")

filename = './json_data/stats.json';

with open(filename, 'w') as jsonFile:
    json.dump(playerTeamMates, jsonFile, indent=4, sort_keys=True)




