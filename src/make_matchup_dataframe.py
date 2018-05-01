import pandas as pd
import os


def get_match_history(gr_df, date, team1, team2):
    return


def main():
    pd.set_option('expand_frame_repr', False)
    pd.set_option('display.max_columns', 500)

    seasons = []
    for year in os.listdir("../dataframes"):
        if not year.startswith('.'):
            seasons.append(year)

    # seasons = ["2010"]

    # for season in seasons:
        # gr_df = pd.read_pickle("../dataframes/" + season + "/" + season + "_game_results")


    season = "2010"
    tr_df = pd.read_pickle("../dataframes/" + season + "/" + season + "_team_records")
    # ts_df = pd.read_pickle("../dataframes/" + season + "/" + season + "_team_streak")
    print(tr_df)
    # tr_df.merge(ts_df, on=["date", "team"], how="inner").to_pickle("../dataframes/" + season + "/" + season + "_team_records")


if __name__ == "__main__":
    main()