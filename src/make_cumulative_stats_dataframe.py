# NBA Game Predictor
# File: json_parser.py
# Authors: Tarmily Wen & Andrew Petrosky
#
# From the dataframes of raw data, it is further refined by creating season-to-date stats

import pandas as pd
from src.data import Data


def get_roster_from_most_recent_game(tp_df, team, date):
    last_played = tp_df[(tp_df['team'] == team) & (tp_df['date'] < date)].max()['date']
    return tp_df[(tp_df['team'] == team) & (tp_df['date'] == last_played)]



def player_season_to_date_stat(ps_df, p_name, game_date):
    game_stats = ps_df[(ps_df['name'] == p_name) & (ps_df['date'] < game_date)]
    # stats_to_accumulate = ['ast', ]

    for index, row in game_stats.iterrows():
        print(row)


    print(game_stats)


def main():
    pd.set_option('expand_frame_repr', False)
    pd.set_option('display.max_columns', 500)

    game_results_df = pd.read_pickle("../dataframes/2010/2010_game_results")
    player_game_stats_df = pd.read_pickle("../dataframes/2010/2010_individual_player_game_stats")
    team_game_stats_df = pd.read_pickle("../dataframes/2010/2010_team_game_stats")
    team_player_df = pd.read_pickle("../dataframes/2010/2010_team_player")

    # print(game_results_df)
    # print(team_game_stats_df)
    # print(player_game_stats_df)
    # print(team_player_df)

    data = Data()

    data.get_vector('20091103', 'Cleveland Cavaliers', 'Washington Wizards', 'win_pct')

    roster_cavs_most_recent = get_roster_from_most_recent_game(team_player_df, 'Cleveland Cavaliers', '20091103')
    roster_wiz_most_recent = get_roster_from_most_recent_game(team_player_df, 'Washington Wizards', '20091103')
    # print(roster_cavs_most_recent)
    # print(roster_wiz_most_recent)
    # player_season_to_date_stat(player_game_stats_df, "James,LeBron", "20091031")


if __name__ == "__main__":
    main()