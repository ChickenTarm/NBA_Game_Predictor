import pandas as pd
import os
from dateutil import parser


def get_match_history(gr_df, date, team1, team2):
    previous_games = gr_df[(((gr_df['home'] == team1) | (gr_df['home'] == team2)) & ((gr_df['away'] == team1) | (gr_df['away'] == team2))) & (gr_df['date'] < date)]
    team1_wins = 0
    team1_win_differential = 0
    team1_lose_differential = 0
    team2_wins = 0
    for index, game in previous_games.iterrows():
        if game["home_score"] > game["away_score"]:
            if game["home"] == team1:
                team1_wins += 1
                team1_win_differential += game["home_score"] - game["away_score"]
            else:
                team2_wins += 1
                team1_lose_differential += game["away_score"] - game["home_score"]
        else:
            if game["away"] == team1:
                team1_wins += 1
                team1_win_differential += game["away_score"] - game["home_score"]
            else:
                team2_wins += 1
                team1_lose_differential += game["home_score"] - game["away_score"]
    if len(previous_games) == 0:
        return team1_wins, team2_wins, team1_win_differential, team1_lose_differential, 0, 0, 0, 0, 0
    else:
        last_game = previous_games.iloc[-1]
        last_game_date = parser.parse(last_game["date"])
        curr_date = parser.parse(date)
        num_days = (curr_date - last_game_date).days
        if last_game["home"] == team1:
            team1_last_differential = last_game["home_score"] - last_game["away_score"]
            if last_game["home_score"] > last_game["away_score"]:
                return team1_wins, team2_wins, team1_win_differential, team1_lose_differential, team1_win_differential / (team1_wins + team2_wins), team1_lose_differential / (team1_wins + team2_wins), team1_last_differential, 1, num_days
            else:
                return team1_wins, team2_wins, team1_win_differential, team1_lose_differential, team1_win_differential / (team1_wins + team2_wins), team1_lose_differential / (team1_wins + team2_wins), team1_last_differential, -1, num_days
        else:
            team1_last_differential = last_game["away_score"] - last_game["home_score"]
            if last_game["away_score"] > last_game["home_score"]:
                return team1_wins, team2_wins, team1_win_differential, team1_lose_differential, team1_win_differential / (team1_wins + team2_wins), team1_lose_differential / (team1_wins + team2_wins), team1_last_differential, 1, num_days
            else:
                return team1_wins, team2_wins, team1_win_differential, team1_lose_differential, team1_win_differential / (team1_wins + team2_wins), team1_lose_differential / (team1_wins + team2_wins), team1_last_differential, -1, num_days


def main():
    pd.set_option('expand_frame_repr', False)
    pd.set_option('display.max_columns', 500)

    seasons = []
    for year in os.listdir("../dataframes"):
        if not year.startswith('.'):
            seasons.append(year)

    # seasons = ["2010"]

    for season in seasons:
        matchup_dict = {"date": [], "home": [], "away": [], "home_wins": [], "away_wins": [], "home_win_t_diff": [], "home_lose_t_diff": [], "home_win_avg_diff": [], "home_lose_avg_diff": [], "home_prev_diff": [], "home_prev_win": [], "last_match": []}
        gr_df = pd.read_pickle("../dataframes/" + season + "/" + season + "_game_results")
        for index, game in gr_df.iterrows():
            date = game["date"]
            team1 = game["home"]
            team2 = game["away"]
            home_wins, away_wins, home_win_diff, home_lose_diff, home_win_diff_avg, home_lose_diff_avg, home_prev_diff, home_prev_win, num_days = get_match_history(gr_df, date, team1, team2)
            matchup_dict["date"].append(date)
            matchup_dict["home"].append(team1)
            matchup_dict["away"].append(team2)
            matchup_dict["home_wins"].append(home_wins)
            matchup_dict["away_wins"].append(away_wins)
            matchup_dict["home_win_t_diff"].append(home_win_diff)
            matchup_dict["home_lose_t_diff"].append(home_lose_diff)
            matchup_dict["home_win_avg_diff"].append(home_win_diff_avg)
            matchup_dict["home_lose_avg_diff"].append(home_lose_diff_avg)
            matchup_dict["home_prev_diff"].append(home_prev_diff)
            matchup_dict["home_prev_win"].append(home_prev_win)
            matchup_dict["last_match"].append(num_days)
        matchup_df = pd.DataFrame(matchup_dict)
        # print(matchup_df)
        matchup_df.to_pickle("../dataframes/" + season + "/" + season + "_matchup_history")


if __name__ == "__main__":
    main()