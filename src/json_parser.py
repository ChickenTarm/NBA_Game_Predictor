# NBA Game Predictor
# File: json_parser.py
# Authors: Andrew Petrosky & Tarmily Wen
#
# Parse the seasons into dicts for a pandas
# dataframe. Returns playoffs start data with
# each seasons dict.

import json
import os


def parse(season):
    games = {}
    prefix = "../data/" + season + "/"
    for game_file in os.listdir(prefix):
        game_file = os.fsdecode(game_file)
        if game_file[-5:] != ".json":
            continue
        with open(prefix + game_file) as game:
            game_json = game.read()
            game_dict = json.loads(game_json)

            # From game_data a (dict of (file name w/o .json) ->
            # (dict of (home, away, homePlayers, awayPlayers) -> stats dict))
            game_key = game_file[:-5]
            game_data = {}
            game_data["home"] = {"team": game_dict["home"], "score": int(game_dict["home_score"]),
                                 "shooting": game_dict["home_shooting"]}
            game_data["away"] = {"team": game_dict["away"], "score": int(game_dict["away_score"]),
                                 "shooting": game_dict["away_shooting"]}

            # If a player does not play, the stats value for them will be set to None
            dnp = ["Did Not Play", "Did Not Dress", "Player Suspended", "Not With Team"]

            home_players = {}
            for (player, stats) in game_dict["home_team"].items():
                for (stat, stat_v) in stats.items():
                    if stat_v in dnp:
                        stats = None
                        break
                    elif stat_v == "":
                        stats[stat] = 0.0
                    elif stat != "mp":
                        stats[stat] = float(stat_v)
                    else:
                        mins = float(stat_v[:-3])
                        secs = float(stat_v[-2:]) / 60.0
                        stats[stat] = mins + secs
                home_players[player] = stats
            game_data["home_players"] = home_players

            away_players = {}
            for (player, stats) in game_dict["away_team"].items():
                for (stat, stat_v) in stats.items():
                    if stat_v in dnp:
                        stats = None
                        break
                    elif stat_v == "":
                        stats[stat] = 0.0
                    elif stat != "mp":
                        stats[stat] = float(stat_v)
                    else:
                        mins = float(stat_v[:-3])
                        secs = float(stat_v[-2:]) / 60.0
                        stats[stat] = mins + secs
                away_players[player] = stats
            game_data["away_players"] = away_players

            games[game_key] = game_data
    return games


def parse_seasons():
    seasons = [("2010", "201004170ATL"), ("2011", "201104160CHI"), ("2012", "201204280CHI"), ("2013", "201304200BRK"),
               ("2014", "201404190IND"), ("2015", "201504180CHI"), ("2016", "201604160ATL"), ("2017", "201704150CLE")]
    season_stats = {}
    for (season, playoffs) in seasons:
        season_dat = parse(season)
        season_stats[season] = (playoffs, season_dat)
    return season_stats
