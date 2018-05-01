# NBA Game Predictor
# File: json_parser.py
# Authors: Tarmily Wen & Andrew Petrosky
#
# From the dataframes of raw data, it is further refined by creating season-to-date stats

import pandas as pd
import time
from argparse import ArgumentParser


def get_roster_from_most_recent_game(tp_df, team, date):
    last_played = tp_df[(tp_df['team'] == team) & (tp_df['date'] < date)].max()['date']
    return tp_df[(tp_df['team'] == team) & (tp_df['date'] == last_played)]



def player_season_to_date_stat(ps_df, gr_df, tgs_df, tp_df, p_name, game_date, c_keys):
    game_stats = ps_df[(ps_df['name'] == p_name) & (ps_df['date'] < game_date)]
    game_c_stats = ps_df[(ps_df['name'] == p_name) & (ps_df['date'] < game_date)][c_keys].sum()

    num_games = len(game_stats)

    if num_games == 0:
        return {}

    teams = tp_df[(tp_df['player'] == p_name) & (tp_df['date'] < game_date)]

    total_team_stats = {'drb': 0, 'fg': 0, 'fg3a': 0, 'fga': 0, 'fta': 0, 'mp': 0, 'orb': 0, 'tov': 0}
    total_opp_stats = {'drb': 0, 'fg': 0, 'fg3a': 0, 'fga': 0, 'fta': 0, 'mp': 0, 'orb': 0, 'tov': 0}

    for index, entry in teams.iterrows():
        team = entry["team"]
        date = entry["date"]
        game = gr_df[((gr_df['home'] == team) | (gr_df['away'] == team)) & (gr_df['date'] == date)]
        if game['home'].values[0] == team:
            opp = game['away'].values[0]
        else:
            opp = game['home'].values[0]
        team_game_stat = tgs_df[(tgs_df['date'] == date) & (tgs_df['team'] == team)]
        opp_game_stat = tgs_df[(tgs_df['date'] == date) & (tgs_df['team'] == opp)]
        for stat in total_team_stats:
            total_team_stats[stat] += team_game_stat[stat].values[0]
            total_opp_stats[stat] += opp_game_stat[stat].values[0]

    cumulative_stats = {}

    for key in game_c_stats.keys():
        cumulative_stats[key] = game_c_stats[key]

    opp_poss = .5 * ((total_opp_stats["fga"] + .4 * total_opp_stats["fta"] - 1.07 * (total_opp_stats["orb"] / (total_opp_stats["orb"] + total_team_stats["orb"])) * (total_opp_stats["fga"] - total_opp_stats["fg"]) + total_opp_stats["tov"]) + (total_team_stats["fga"] + .4 * total_team_stats["fta"] - 1.07 * (total_team_stats["orb"] / (total_team_stats["orb"] + total_opp_stats["drb"])) * (total_team_stats["fga"] - total_team_stats["fg"]) + total_team_stats["tov"]))

    cumulative_stats["ast_pg"] = cumulative_stats["ast"] / num_games
    cumulative_stats["blk_pg"] = cumulative_stats["blk"] / num_games
    cumulative_stats["def_rtg_pg"] = cumulative_stats["def_rtg"] / num_games
    cumulative_stats["drb_pg"] = cumulative_stats["drb"] / num_games
    cumulative_stats["fg_pg"] = cumulative_stats["fg"] / num_games
    cumulative_stats["fg3_pg"] = cumulative_stats["fg3"] / num_games
    cumulative_stats["fg3a_pg"] = cumulative_stats["fg3a"] / num_games
    cumulative_stats["fga_pg"] = cumulative_stats["fga"] / num_games
    cumulative_stats["ft_pg"] = cumulative_stats["ft"] / num_games
    cumulative_stats["fta_pg"] = cumulative_stats["fta"] / num_games
    cumulative_stats["mp_pg"] = cumulative_stats["mp"] / num_games
    cumulative_stats["off_rtg_pg"] = cumulative_stats["off_rtg"] / num_games
    cumulative_stats["orb_pg"] = cumulative_stats["orb"] / num_games
    cumulative_stats["pf_pg"] = cumulative_stats["pf"] / num_games
    cumulative_stats["plus_minus"] = cumulative_stats["plus_minus"] / num_games
    cumulative_stats["pts_pg"] = cumulative_stats["pts"] / num_games
    cumulative_stats["stl_pg"] = cumulative_stats["stl"] / num_games
    cumulative_stats["tov_pg"] = cumulative_stats["tov"] / num_games
    cumulative_stats["trb_pg"] = cumulative_stats["trb"] / num_games
    cumulative_stats["ast_pct"] = 100 * cumulative_stats["ast"] / (((cumulative_stats["mp"] / (total_team_stats["mp"] / 5)) * total_team_stats["fg"]) - cumulative_stats["fg"])
    cumulative_stats["blk_pct"] = 100 * (cumulative_stats["blk"] * (total_team_stats["mp"] / 5)) / (cumulative_stats["mp"] * (total_opp_stats["fga"] - total_opp_stats["fg3a"]))
    cumulative_stats["drb_pct"] = 100 * (cumulative_stats["drb"] * (total_team_stats["mp"] / 5)) / (cumulative_stats["mp"] * (total_team_stats["drb"] + total_opp_stats["orb"]))
    cumulative_stats["efg_pct"] = 100 * (cumulative_stats["fg"] + .5 * cumulative_stats["fg3"]) / cumulative_stats["fga"]
    cumulative_stats["fg3_pct"] = 100 * (cumulative_stats["fg3"] / cumulative_stats["fg3a"])
    cumulative_stats["fg3a_per_fga_pct"] = 100 * cumulative_stats["fg3a"] / cumulative_stats["fga"]
    cumulative_stats["fg_pct"] = 100 * cumulative_stats["fg"] / cumulative_stats["fga"]
    cumulative_stats["ft_pct"] = 100 * cumulative_stats["ft"] / cumulative_stats["fta"]
    cumulative_stats["fta_per_fga_pct"] = 100 * cumulative_stats["fta"] / cumulative_stats["fga"]
    cumulative_stats["orb_pct"] = 100 * (cumulative_stats["orb"] * (total_team_stats["mp"] / 5)) / (cumulative_stats["mp"] * (total_team_stats["orb"] + total_opp_stats["drb"]))
    cumulative_stats["stl_pct"] = 100 * (cumulative_stats["stl"] * (total_team_stats["mp"] / 5)) / (cumulative_stats["mp"] * opp_poss)
    cumulative_stats["tov_pct"] = 100 * cumulative_stats["tov"] / (cumulative_stats["fga"] + .44 * cumulative_stats["fta"] + cumulative_stats["tov"])
    cumulative_stats["trb_pct"] = 100 * ((cumulative_stats["orb"] + cumulative_stats["drb"]) * (total_team_stats["mp"] / 5)) / (cumulative_stats["mp"] * (total_team_stats["orb"] + total_team_stats["drb"] + total_opp_stats["orb"] + total_opp_stats["drb"]))
    cumulative_stats["ts_pct"] = 100 * cumulative_stats["pts"] / (2 * (cumulative_stats["fga"] + .44 * cumulative_stats["fta"]))
    cumulative_stats["usg_pct"] = 100 * ((cumulative_stats["fga"] + .44 * cumulative_stats["fta"] + cumulative_stats["tov"]) * (total_team_stats["mp"] / 5)) / (cumulative_stats["mp"] * (total_team_stats["fga"] + .44 * total_team_stats["fta"] + total_team_stats["tov"]))

    # print(cumulative_stats)
    #
    # print(game_stats)
    # print(len(cumulative_stats.keys()))
    return cumulative_stats


def main():
    parser = ArgumentParser()
    parser.add_argument("-season", default="2017")
    args = parser.parse_args()

    season = args.season

    pd.set_option('expand_frame_repr', False)
    pd.set_option('display.max_columns', 500)

    # for year in os.listdir("../dataframes"):
    #     if not year.startswith('.'):
    #         season = year

    game_results_df = pd.read_pickle("../dataframes/" + season + "/" + season + "_game_results")
    player_game_stats_df = pd.read_pickle("../dataframes/" + season + "/" + season + "_individual_player_game_stats")
    team_game_stats_df = pd.read_pickle("../dataframes/" + season + "/" + season + "_team_game_stats")
    team_player_df = pd.read_pickle("../dataframes/" + season + "/" + season + "_team_player")

    cumulative_keys = [key for key in player_game_stats_df.keys() if "pct" not in key]
    cumulative_keys.remove("name")
    cumulative_keys.remove("date")

    print(cumulative_keys)

    cum_stat_names = ['name', 'date', 'ast', 'blk', 'def_rtg', 'drb', 'fg', 'fg3', 'fg3a', 'fga', 'ft', 'fta', 'mp',
                      'off_rtg', 'orb', 'pf', 'plus_minus', 'pts', 'stl', 'tov', 'trb', 'ast_pg', 'blk_pg', 'def_rtg_pg', 'drb_pg', 'fg_pg',
                      'fg3_pg', 'fg3a_pg', 'fga_pg', 'ft_pg', 'fta_pg', 'mp_pg', 'off_rtg_pg', 'orb_pg', 'pf_pg', 'pts_pg', 'stl_pg',
                      'tov_pg', 'trb_pg', 'ast_pct', 'blk_pct', 'drb_pct', 'efg_pct', 'fg3_pct', 'fg3a_per_fga_pct', 'fg_pct', 'ft_pct',
                      'fta_per_fga_pct', 'orb_pct', 'stl_pct', 'tov_pct', 'trb_pct', 'ts_pct', 'usg_pct']

    cum_stats = {key: [] for key in cum_stat_names}

    # roster_cavs_most_recent = get_roster_from_most_recent_game(team_player_df, 'Cleveland Cavaliers', '20091103')
    # roster_wiz_most_recent = get_roster_from_most_recent_game(team_player_df, 'Washington Wizards', '20091103')

    players_list = player_game_stats_df.name.unique()

    print(len(players_list))

    # players_list = ["James,LeBron"]

    count = 0

    start = time.time()

    for player_name in players_list:
        print("player_" + str(count) + ": " + player_name)
        player_games_date = player_game_stats_df[player_game_stats_df["name"] == player_name]["date"].values
        count += 1
        for date in player_games_date:
            cum_vector = player_season_to_date_stat(player_game_stats_df, game_results_df, team_game_stats_df, team_player_df, player_name, date, cumulative_keys)
            for key in cum_stats:
                if key == "name":
                    cum_stats["name"].append(player_name)
                elif key == "date":
                    cum_stats["date"].append(date)
                else:
                    if not cum_vector:
                        cum_stats[key].append(0)
                    else:
                        cum_stats[key].append(cum_vector[key])

    end = time.time()

    print("time: " + str(end - start))

    cum_df = pd.DataFrame(cum_stats)

    cum_df = cum_df.fillna(0)

    cum_df.to_pickle("../dataframes/" + str(season) + "/" + str(season) + "_season_to_date_player_stats")

    # print(cum_df)


if __name__ == "__main__":
    main()