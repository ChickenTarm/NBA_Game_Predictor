# NBA Game Predictor
# File: json_parser.py
# Authors: Tarmily Wen & Andrew Petrosky
#
# Takes the parsed seasons and creates dataframes from them

import pandas as pd
import src.json_parser as jp
from collections import OrderedDict


def player_stat_dict():
    return {'name': [], 'date': [], 'mp': [], 'fg': [], 'fga': [], 'fg_pct': [], 'fg3': [], 'fg3a': [], 'fg3_pct': [], 'ft': [], 'fta': [], 'ft_pct': [], 'orb': [], 'drb': [], 'trb': [], 'ast': [], 'stl': [], 'blk': [], 'tov': [], 'pf': [], 'pts': [], 'plus_minus': [], 'ts_pct': [], 'efg_pct': [], 'fg3a_per_fga_pct': [], 'fta_per_fga_pct': [], 'orb_pct': [], 'drb_pct': [], 'trb_pct': [], 'ast_pct': [], 'stl_pct': [], 'blk_pct': [], 'tov_pct': [], 'usg_pct': [], 'off_rtg': [], 'def_rtg': []}


def team_player_dict():
    return {'team': [], 'player': [], 'date': []}


def team_game_dict():
    return {'team': [], 'date': [], 'fg': [], 'fga': [], 'fta': [], 'mp': [], 'tov': [], 'orb': [], 'drb': [], 'fg3a': []}


def add_to_player_dict(pd, players, date):
    team_stats = {'fg': 0, 'fga': 0, 'fta': 0, 'mp': 0, 'tov': 0, 'orb': 0, 'drb': 0, 'fg3a': 0}
    for name in players:
        stats = players[name]
        for key in pd.keys():
            if key=='name':
                pd[key].append(name)
            elif key=='date':
                pd[key].append(date)
            else:
                if stats==None:
                    pd[key].append(None)
                else:
                    if key in team_stats:
                        team_stats[key] += stats[key]
                    pd[key].append(stats[key])
    return team_stats


def add_to_team_stat_dict(tsd, ts):
    for stat in ts:
        tsd[stat].append(ts[stat])


def main():
    pd.set_option('expand_frame_repr', False)
    pd.set_option('display.max_columns', 500)

    seasons = jp.parse_seasons()
    for season in seasons:
        # playoff_start = seasons[season][0][0:8]
        sorted_games = OrderedDict(sorted(seasons[season][1].items(), key=lambda x:x[0]))
        game_dates = list(sorted_games.keys())
        game_stats = list(sorted_games.values())
        num_games = len(game_dates)
        player_game_stats = player_stat_dict()
        team_players = team_player_dict()
        team_game_stats = team_game_dict()
        game_results = {'date': [], 'home': [], 'away': [], "home_score": [], "away_score": []}
        for i in range(0, num_games):
            date = game_dates[i][0:8]
            home_stats = game_stats[i]["home"]
            away_stats = game_stats[i]["away"]
            home_players = game_stats[i]["home_players"]
            away_players = game_stats[i]["away_players"]

            num_home_players = len(home_players.keys())
            team_players['team'] += [home_stats['team']] * num_home_players
            team_players['player'] += home_players.keys()
            team_players['date'] += [date] * len(home_players.keys())

            num_away_players = len(away_players.keys())
            team_players['team'] += [away_stats['team']] * num_away_players
            team_players['player'] += away_players.keys()
            team_players['date'] += [date] * num_away_players

            home_team_stats = add_to_player_dict(player_game_stats, home_players, date)
            away_team_stats = add_to_player_dict(player_game_stats, away_players, date)

            home_team_stats['team'] = home_stats['team']
            home_team_stats['date'] = date

            away_team_stats['team'] = away_stats['team']
            away_team_stats['date'] = date

            add_to_team_stat_dict(team_game_stats, home_team_stats)
            add_to_team_stat_dict(team_game_stats, away_team_stats)

            game_results['date'].append(date)
            game_results['home'].append(home_stats['team'])
            game_results['away'].append(away_stats['team'])
            game_results['home_score'].append(home_stats['score'])
            game_results['away_score'].append(away_stats['score'])

        player_game_df = pd.DataFrame(player_game_stats)
        team_player_df = pd.DataFrame(team_players)
        game_results_df = pd.DataFrame(game_results)
        team_game_stats_df = pd.DataFrame(team_game_stats)

        player_game_df.to_pickle("../dataframes/" + str(season) + "/" + str(season) + "_individual_player_game_stats")
        team_player_df.to_pickle("../dataframes/" + str(season) + "/" + str(season) + "_team_player")
        game_results_df.to_pickle("../dataframes/" + str(season) + "/" + str(season) + "_game_results")
        team_game_stats_df.to_pickle("../dataframes/" + str(season) + "/" + str(season) + "_team_game_stats")

        # print(game_results_df)
        # print(team_game_stats_df)
        #
        # roster_cavs_most_recent = get_roster_from_most_recent_game(team_player_df, 'Cleveland Cavaliers', '20091031')
        # print(roster_cavs_most_recent)
        # player_season_to_date_stat(player_game_df, 'James,LeBron', '20091031')



if __name__ == "__main__":
    main()