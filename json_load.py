import pandas as pd

STATS_ELEMENT = 'stats'
PLAYER_A_ID = 251

PATH_FORMAT = "./json_data/stats_%s.json"

SEASONS = ["2018-19", "2017-18", "2016-17"]
players_stats_dic = {}

for season in SEASONS:
    print("Getting data for season: ",season)
    filename = PATH_FORMAT % season
    players_data_frame = pd.read_json(filename)
    for frame in players_data_frame:
        player_frame = pd.DataFrame.from_dict(players_data_frame[frame][STATS_ELEMENT], orient='columns')
        if not player_frame.empty:
            player_frame = player_frame.drop(columns=['kickoff_time', 'kickoff_time_formatted']).dropna()
            if frame in players_stats_dic:
                players_stats_dic[frame] = pd.concat([players_stats_dic[frame], player_frame])
            else:
                players_stats_dic[frame] = player_frame

import numpy as np
from sklearn.linear_model import LinearRegression

player_A = players_stats_dic.pop(PLAYER_A_ID)
player_A_points = player_A['goals_scored']

player_A_points_train = player_A_points[:80]
player_A_points_test = player_A_points[80:]

for i in range(200, 600):
    if i in players_stats_dic:
        correlated_player = players_stats_dic[i][["influence"]]
        if np.size(correlated_player,axis=0) == player_A_points.size:
            correlated_player_train = correlated_player[:80]
            correlated_player_test = correlated_player[80:]

            regression_model = LinearRegression().fit(correlated_player_train, player_A_points_train)
            print('Id : ', i, ', Name : ', players_data_frame[i]['name'], ', Coeff : ', regression_model.coef_, ', Score :',
                regression_model.score(correlated_player_test, player_A_points_test))
