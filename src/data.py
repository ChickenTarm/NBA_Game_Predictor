import pandas as pd
from collections import OrderedDict
import os
import time
import numpy as np


class Data(object):

    def __init__(self):
        self.data_dict = {}

        for year in os.listdir("../dataframes"):
            if not year.startswith('.'):
                self.data_dict[year] = {}
                for df in os.listdir("../dataframes/" + year):
                    df_path = "../dataframes/" + year + "/" + df
                    if "results" in df:
                        self.data_dict[year]["gr_df"] = pd.read_pickle(df_path)
                    elif "individual" in df:
                        self.data_dict[year]["ipgs_df"] = pd.read_pickle(df_path)
                    elif "team_game" in df:
                        self.data_dict[year]["tgs_df"] = pd.read_pickle(df_path)
                    elif "team_player" in df:
                        self.data_dict[year]["tp_df"] = pd.read_pickle(df_path)
                    elif "team_records" in df:
                        self.data_dict[year]["tr_df"] = pd.read_pickle(df_path)
                    elif "season_to_date" in df:
                        self.data_dict[year]["std_df"] = pd.read_pickle(df_path)

    def get_starters_from_last_game(self, tp_df, ipgs_df, date, team):
        most_recent = tp_df[(tp_df["team"] == team) & (tp_df['date'] < date)]["date"].max()
        players = tp_df[(tp_df["team"] == team) & (tp_df['date'] == most_recent)][["player", "date"]]
        player_names = players["player"].values
        # print(players["player"])
        # print("James,LeBron" in players["player"].values)
        player_minutes = {}
        for name in player_names:
            player_minutes[name] = ipgs_df[(ipgs_df["name"] == name) & (ipgs_df["date"] == most_recent)]["mp"].values[0]
            # player_stats = ipgs_df[(ipgs_df["name"] == name) & (ipgs_df["date"] == most_recent)]
        player_minutes = OrderedDict(sorted(player_minutes.items(), key=lambda x: x[1], reverse=True))
        return list(player_minutes.keys())[0:5]

    def get_starter_stats(self, std_df, date, players):
        team_stats = []
        for player in players:
            team_stats += list(std_df[(std_df["name"] == player) & (std_df["date"] <= date)].iloc[-1].drop(["name", "date"]).values)
        return team_stats

    def get_record_from_most_recent_games(self, tr_df, team, date):
        record = tr_df[(tr_df['team'] == team) & (tr_df['date'] <= date)]
        if len(record) == 0:
            return 0, 0, 0, 0, 0
        else:
            record = record.iloc[-1]
            return record["home_wins"], record["home_losses"], record["away_wins"], record["home_losses"], record["win_pct"]

    def get_vector(self, date, home, away, season, form):
        if (form == "win_pct"):
            home_hw, home_hl, home_aw, home_al, home_wp = self.get_record_from_most_recent_games(self.data_dict[season]["tr_df"], home, date)
            away_hw, away_hl, away_aw, away_al, away_wp = self.get_record_from_most_recent_games(self.data_dict[season]["tr_df"], away, date)
            return [home_wp, away_wp]
        if (form == "record"):
            home_hw, home_hl, home_aw, home_al, home_wp = self.get_record_from_most_recent_games(self.data_dict[season]["tr_df"], home, date)
            away_hw, away_hl, away_aw, away_al, away_wp = self.get_record_from_most_recent_games(self.data_dict[season]["tr_df"], away, date)
            return [home_hw, home_hl, home_aw, home_al, home_wp, away_hw, away_hl, away_aw, away_al, away_wp]
        if (form == "rec_cum_stat"):
            home_starters = self.get_starters_from_last_game(self.data_dict[season]["tp_df"], self.data_dict[season]["ipgs_df"], date, home)
            away_starters = self.get_starters_from_last_game(self.data_dict[season]["tp_df"], self.data_dict[season]["ipgs_df"], date, away)
            home_stats = self.get_starter_stats(self.data_dict[season]["std_df"], date, home_starters)
            away_stats = self.get_starter_stats(self.data_dict[season]["std_df"], date, away_starters)
            record = self.get_vector(date, home, away, season, "record")
            return record + home_stats + away_stats

    def get_season_data(self, season, form):
        X = []
        Y = []
        for index, game in self.data_dict[season]["gr_df"].iterrows():
            X.append(self.get_vector(game["date"], game["home"], game["away"], season, form))
            if game["home_score"] > game["away_score"]:
                Y.append(1)
            else:
                Y.append(0)
        return X, Y


def main():
    pd.set_option('expand_frame_repr', False)
    pd.set_option('display.max_columns', 500)

    data = Data()

    # season = "2010"
    #
    # team_player_df = pd.read_pickle("../dataframes/" + season + "/" + season + "_team_player")
    #
    # player_game_stats_df = pd.read_pickle("../dataframes/" + season + "/" + season + "_individual_player_game_stats")
    #
    # season_to_date_df = pd.read_pickle("../dataframes/" + season + "/" + season + "_season_to_date_player_stats")
    #
    # # print(player_game_stats_df)
    #
    # home_players = data.get_starters_from_last_game(team_player_df, player_game_stats_df, "20091114", "Cleveland Cavaliers")
    #
    # home_stats = data.get_starter_stats(season_to_date_df, "20091114", home_players)
    #
    # vect = data.get_vector("20091114", "Cleveland Cavaliers", "Utah Jazz", "2010", "rec_cum_stat")

    seasons = []
    for year in os.listdir("../dataframes"):
        if not year.startswith('.'):
            seasons.append(year)

    for season in seasons:
        X, Y = data.get_season_data(season, "rec_cum_stat")

        np_x = np.array(X)
        np_y = np.array(Y)

        np.save("../labels/" + season + "/" + season + "_rec_cum_stat_vectors", np_x)
        np.save("../labels/" + season + "/" + season + "_labels", np_y)

if __name__ == "__main__":
    main()
