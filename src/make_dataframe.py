import pandas as pd
import src.json_parser as jp
from collections import OrderedDict
import random


def player_stat_dict():
    return {'name': [], 'date': [], 'mp': [], 'fg': [], 'fga': [], 'fg_pct': [], 'fg3': [], 'fg3a': [], 'fg3_pct': [], 'ft': [], 'fta': [], 'ft_pct': [], 'orb': [], 'drb': [], 'trb': [], 'ast': [], 'stl': [], 'blk': [], 'tov': [], 'pf': [], 'pts': [], 'plus_minus': [], 'ts_pct': [], 'efg_pct': [], 'fg3a_per_fga_pct': [], 'fta_per_fga_pct': [], 'orb_pct': [], 'drb_pct': [], 'trb_pct': [], 'ast_pct': [], 'stl_pct': [], 'blk_pct': [], 'tov_pct': [], 'usg_pct': [], 'off_rtg': [], 'def_rtg': []}


def team_player_dict():
    return {'team': [], 'players': [], 'date': []}


def add_to_player_dict(pd, players, date):
    for name in players:
        stats = players[name]
        print(name)
        print(stats)
        for key in pd.keys():
            if key=='name':
                pd[key].append(name)
            elif key=='date':
                pd[key].append(date)
            else:
                if stats==None:
                    pd[key].append(None)
                else:
                    pd[key].append(stats[key])


def main():
    pd.set_option('expand_frame_repr', False)

    seasons = jp.parse_seasons()
    for season in ["2010"]:
        playoff_start = seasons[season][0]
        sorted_games = OrderedDict(sorted(seasons[season][1].items(), key=lambda x:x[0]))
        game_dates = list(sorted_games.keys())
        game_stats = list(sorted_games.values())
        num_games = len(game_dates)
        player_stats = player_stat_dict()
        team_players = team_player_dict()
        print(player_stats)
        for i in range(0, 1):
            date = game_dates[i][0:8]
            home_stats = game_stats[i]["home"]
            away_stats = game_stats[i]["away"]
            home_players = game_stats[i]["home_players"]
            away_players = game_stats[i]["away_players"]
            # print(date)
            # print(home_stats)
            # print(away_stats)
            # print(home_players)
            # print(home_player_stats)
            # print(away_players)
            # print(away_player_stats)
            add_to_player_dict(player_stats, home_players, date)
            add_to_player_dict(player_stats, away_players, date)
        player_df = pd.DataFrame(player_stats)
        player_df = player_df.set_index(['name', 'date'])
        print(player_df)


if __name__ == "__main__":
    main()