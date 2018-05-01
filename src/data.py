import pandas as pd
import os


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

    def get_record_from_most_recent_games(self, tr_df, team, date):
        # games_played = tp_df[((tp_df['home'] == team) | (tp_df['away'] == team)) & (tp_df['date'] < date)]
        # num_games = 0
        # home_wins = 0
        # away_wins = 0
        # home_losses = 0
        # away_losses = 0
        # for index, row in games_played.iterrows():
        #     num_games += 1
        #     if row["home"] == team:
        #         if row["home_score"] > row["away_score"]:
        #             home_wins += 1
        #         else:
        #             home_losses += 1
        #     else:
        #         if row["home_score"] < row["away_score"]:
        #             away_wins += 1
        #         else:
        #             away_losses += 1
        # if num_games == 0:
        #     win_pct = 0
        # else:
        #     win_pct = (home_wins + away_wins) / num_games
        most_recent = tr_df[(tr_df['team'] == team) & (tr_df['date'] <= date)]["date"].max()
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

    def get_season_data(self, season, form):
        X = []
        Y = []
        for index, game in self.data_dict[season]["gr_df"].iterrows():
            X.append(self.get_vector(game["date"], game["home"], game["away"], season, form))
            if game["home_score"] > game["away_score"]:
                Y.append(1)
            else:
                Y.append(0)
            # if index == 38:
            #     print(game["date"])
            #     print(game["home"])
            #     print(game["away"])
            #     print(X[index])
            #     print(Y[index])
        return X, Y
