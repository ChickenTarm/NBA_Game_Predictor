# NBA Game Predictor
# File: json_parser.py
# Authors: Andrew Petrosky & Tarmily Wen
#
# Provides a function which takes in a season string,
# loads the appropriate games from the season, and returns
# a tuple of two lists of dictionaries representing games in
# date order, one of which is regular season and the other
# is playoffs

import json
import os


def parse(season, season_type):
    games = []
    prefix = "../data/nba/" + season + "/" + season_type + "/"
    for game_file in os.listdir(prefix):
        game_file = os.fsdecode(game_file)
        with open(prefix + game_file) as game:
            game_json = game.read()
            game_data = json.loads(game_json)
            games += [game_data]
    return games


def parse_season(season):
    regular_season = parse(season, "regular")
    post_season = parse(season, "playoffs")
    return regular_season, post_season
