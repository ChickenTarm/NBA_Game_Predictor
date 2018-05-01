import pandas as pd
import os


def get_record(gr_df, date, team):
    games_played = gr_df[((gr_df['home'] == team) | (gr_df['away'] == team)) & (gr_df['date'] < date)]
    num_games = 0
    home_wins = 0
    away_wins = 0
    home_losses = 0
    away_losses = 0
    for index, row in games_played.iterrows():
        num_games += 1
        if row["home"] == team:
            if row["home_score"] > row["away_score"]:
                home_wins += 1
            else:
                home_losses += 1
        else:
            if row["home_score"] < row["away_score"]:
                away_wins += 1
            else:
                away_losses += 1
    if num_games == 0:
        win_pct = 0
    else:
        win_pct = (home_wins + away_wins) / num_games
    return home_wins, home_losses, away_wins, away_losses, win_pct

def main():
    pd.set_option('expand_frame_repr', False)
    pd.set_option('display.max_columns', 500)

    seasons = []
    for year in os.listdir("../dataframes"):
        if not year.startswith('.'):
            seasons.append(year)
    for season in seasons:
        team_records = {"team": [], "date": [], "home_wins": [], "home_losses": [], "away_wins": [], "away_losses": [], "win_pct": []}
        game_results_df = pd.read_pickle("../dataframes/" + season + "/" + season + "_game_results")
        for index, row in game_results_df.iterrows():
            date = row["date"]
            home = row["home"]
            away = row["away"]
            home_hw, home_hl, home_aw, home_al, home_wp = get_record(game_results_df, date, home)
            away_hw, away_hl, away_aw, away_al, away_wp = get_record(game_results_df, date, away)
            team_records["date"].append(date)
            team_records["team"].append(home)
            team_records["home_wins"].append(home_hw)
            team_records["home_losses"].append(home_hl)
            team_records["away_wins"].append(home_aw)
            team_records["away_losses"].append(home_al)
            team_records["win_pct"].append(home_wp)

            team_records["date"].append(date)
            team_records["team"].append(away)
            team_records["home_wins"].append(away_hw)
            team_records["home_losses"].append(away_hl)
            team_records["away_wins"].append(away_aw)
            team_records["away_losses"].append(away_al)
            team_records["win_pct"].append(away_wp)

        record_df = pd.DataFrame(team_records)
        record_df.to_pickle("../dataframes/" + season + "/" + season + "_team_records")


if __name__ == "__main__":
    main()