import pandas as pd
import os


def get_streak(gr_df, date, team):
    previous_games = gr_df[((gr_df['home'] == team) | (gr_df['away'] == team)) & (gr_df['date'] < date)].iloc[::-1]

    first_game = True
    streak_type = ""

    streak = 0

    for index, game in previous_games.iterrows():
        if game["home"] == team:
            if game["home_score"] > game["away_score"]:
                if first_game:
                    first_game = False
                    streak_type = "win"
                    streak += 1
                else:
                    if streak_type == "win":
                        streak += 1
                    else:
                        return streak
            else:
                if first_game:
                    first_game = False
                    streak_type = "lose"
                    streak += -1
                else:
                    if streak_type == "lose":
                        streak += -1
                    else:
                        return streak
        else:
            if game["away_score"] > game["home_score"]:
                if first_game:
                    first_game = False
                    streak_type = "win"
                    streak += 1
                else:
                    if streak_type == "win":
                        streak += 1
                    else:
                        return streak
            else:
                if first_game:
                    first_game = False
                    streak_type = "lose"
                    streak += -1
                else:
                    if streak_type == "lose":
                        streak += -1
                    else:
                        return streak
    return streak


def main():
    pd.set_option('expand_frame_repr', False)
    pd.set_option('display.max_columns', 500)

    seasons = []
    for year in os.listdir("../dataframes"):
        if not year.startswith('.'):
            seasons.append(year)

    for season in seasons:
        gr_df = pd.read_pickle("../dataframes/" + season + "/" + season + "_game_results")
        streak_dict = {"date": [], "team": [], "streak": []}
        for index, game in gr_df.iterrows():
            date = game["date"]
            home_streak = get_streak(gr_df, date, game["home"])
            away_streak = get_streak(gr_df, date, game["away"])
            streak_dict["date"].append(date)
            streak_dict["team"].append(game["home"])
            streak_dict["streak"].append(home_streak)

            streak_dict["date"].append(date)
            streak_dict["team"].append(game["away"])
            streak_dict["streak"].append(away_streak)

        streak_df = pd.DataFrame(streak_dict)
        streak_df.to_pickle("../dataframes/" + season + "/" + season + "_team_streak")


if __name__ == "__main__":
    main()
