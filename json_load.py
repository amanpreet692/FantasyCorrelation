import pandas as pd

STATS_ELEMENT = 'stats'
PLAYER_A_ID = 251

path = './json_data/stats.json'

players_data_frame = pd.read_json(path, orient='records')

players_stats_dic = {}

for frame in players_data_frame:
    player_frame = pd.DataFrame.from_dict(players_data_frame[frame][STATS_ELEMENT], orient='columns')
    player_frame = player_frame.drop(columns=['kickoff_time', 'kickoff_time_formatted']).dropna()
    if frame == PLAYER_A_ID:
        player_A = player_frame
    players_stats_dic[frame] = player_frame

import numpy as np
from sklearn.linear_model import LinearRegression

player_A_points = player_A['total_points']
print(player_A_points)

player_A_points_train = player_A_points[:25]
player_A_points_test = player_A_points[25:]

for i in range(247, 257):
    correlated_player = players_stats_dic[i][['total_points']]

    correlated_player_train = correlated_player[:25]
    correlated_player_test = correlated_player[25:]

    regression_model = LinearRegression().fit(correlated_player_train, player_A_points_train)
    print('Id : ', i, ', Name : ', players_data_frame[i]['name'],', Coeff : ',regression_model.coef_, ', Score :', regression_model.score(correlated_player_test, player_A_points_test))
