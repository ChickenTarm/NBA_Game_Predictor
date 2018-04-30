import requests
import json
import os
from bs4 import BeautifulSoup
from argparse import ArgumentParser


def box_score_parser(url, season, playoffs):
    bs_resp = requests.get(url)

    if bs_resp.ok:
        bs_parser = BeautifulSoup(bs_resp.text, "html.parser")

        headline = bs_parser.find_all('h1')[0].get_text()

        headline_split = headline.split(' at ')

        away_name = headline_split[0]
        home_name = headline_split[1].split(" Box")[0]

        html_tables = [t.find('tbody') for t in bs_parser.find_all('div', id=lambda x: x and x.startswith("all_box"))]

        away_tables = html_tables[0:2]

        home_tables = html_tables[2:]

        away_team = {}

        home_team = {}

        away_pts = 0

        home_pts = 0

        for table in away_tables:
            players_stats = table.find_all('tr')
            del players_stats[5]
            for player in players_stats:
                name = player.find('th')['csk']
                if name not in away_team:
                    away_team[name] = {}
                for stat in player.find_all('td'):
                    stat_name = stat['data-stat']
                    info = stat.getText()
                    if stat_name == "pts":
                        away_pts += int(info)
                    away_team[name][stat_name] = info

        for table in home_tables:
            players_stats = table.find_all('tr')
            del players_stats[5]
            for player in players_stats:
                name = player.find('th')['csk']
                if name not in home_team:
                    home_team[name] = {}
                for stat in player.find_all('td'):
                    stat_name = stat['data-stat']
                    info = stat.getText()
                    if stat_name == "pts":
                        home_pts += int(info)
                    home_team[name][stat_name] = info

        game = {}

        game["home"] = home_name
        game["away"] = away_name

        game["home_score"] = home_pts
        game["away_score"] = away_pts

        game["home_team"] = home_team
        game["away_team"] = away_team

        last_slash = url.rfind('/')

        shot_chart_url = url[:last_slash + 1] + "shot-chart/" + url[last_slash + 1:]

        file_name = "../data/nba/" + ""

        sc_resp = requests.get(shot_chart_url)

        if sc_resp.ok:
            sc_parser = BeautifulSoup(sc_resp.text, "html.parser")

            sc_tables = sc_parser.select('div table')

            away_shooting = {}

            home_shooting = {}

            away_shooting_table = sc_tables[0]
            home_shooting_table = sc_tables[1]

            quarters = away_shooting_table.find_all('tr')[-4:]
            for quarter in quarters:
                for stat in quarter.find_all('td'):
                    stat_name = stat['data-stat']
                    if "pct" not in stat_name:
                        info = int(stat.getText())
                        if stat_name not in away_shooting:
                            away_shooting[stat_name] = info
                        else:
                            away_shooting[stat_name] += info

            quarters = home_shooting_table.find_all('tr')[-4:]
            for quarter in quarters:
                for stat in quarter.find_all('td'):
                    stat_name = stat['data-stat']
                    if "pct" not in stat_name:
                        info = int(stat.getText())
                        if stat_name not in home_shooting:
                            home_shooting[stat_name] = info
                        else:
                            home_shooting[stat_name] += info

            away_shooting["fg_pct"] = away_shooting["fg"] / away_shooting["fga"]
            away_shooting["fg2_pct"] = away_shooting["fg2"] / away_shooting["fg2a"]
            away_shooting["fg3_pct"] = away_shooting["fg3"] / away_shooting["fg3a"]
            away_shooting["fg_ast_pct"] = away_shooting["fg_ast"] / away_shooting["fg"]
            away_shooting["efg_pct"] = (away_shooting["fg"] + .5 * away_shooting["fg3"]) / away_shooting["fga"]

            home_shooting["fg_pct"] = home_shooting["fg"] / home_shooting["fga"]
            home_shooting["fg2_pct"] = home_shooting["fg2"] / home_shooting["fg2a"]
            home_shooting["fg3_pct"] = home_shooting["fg3"] / home_shooting["fg3a"]
            home_shooting["fg_ast_pct"] = home_shooting["fg_ast"] / home_shooting["fg"]
            home_shooting["efg_pct"] = (home_shooting["fg"] + .5 * home_shooting["fg3"]) / home_shooting["fga"]

            game["home_shooting"] = home_shooting
            game["away_shooting"] = away_shooting
        else:
            print("Bad Shot Chart url: " + url)
    else:
        print("Bad Box Score url: " + url)

    if playoffs:
        json.dump(game, open("../data/nba/" + season + "/playoffs/" + url[last_slash + 1:-5] + ".json", 'w'), indent=4)
    else:
        # json.dump(game, open("../data/nba/" + season + "/regular/" + url[last_slash + 1:-5] + ".json", 'w'), indent=4)
        json.dump(game, open("../data/" + season + "/" + url[last_slash + 1:-5] + ".json", 'w'), indent=4)


def main():

    parser = ArgumentParser()
    parser.add_argument("-season", default="2017")
    args = parser.parse_args()

    season_year = args.season

    season_url = "https://www.basketball-reference.com/leagues/NBA_" + season_year + "_games.html"

    playoffs = False

    resp = requests.get(season_url)

    folder = "../data/" + season_year + "/"
    # reg_folder = "../data/nba/" + season_year + "/regular/"
    # po_folder = "../data/nba/" + season_year + "/playoffs/"
    directory = os.path.dirname(folder)
    # reg_directory = os.path.dirname(reg_folder)
    # po_directory = os.path.dirname(po_folder)

    if not os.path.exists(directory):
          os.makedirs(directory)
    # if not os.path.exists(reg_directory):
    #     os.makedirs(reg_directory)
    # if not os.path.exists(po_directory):
    #     os.makedirs(po_directory)

    if resp.ok:
        season_parser = BeautifulSoup(resp.text, 'html.parser')

        month_buttons = [d.find('a') for d in season_parser.find_all('div', class_='filter')[0].find_all('div')]

        for month in month_buttons:
            month_url = "https://www.basketball-reference.com" + month['href']

            m_resp = requests.get(month_url)

            month_parser = BeautifulSoup(m_resp.text, 'html.parser')

            game_table = month_parser.select('div table tbody')[0]

            game_rows = game_table.find_all('tr')

            for game in game_rows:
                cls = game.get("class")
                # if not cls is None:
                #     playoffs = True
                playoffs = False
                # else:
                bs_url = "https://www.basketball-reference.com" + game.find_all('td')[5].find('a')['href']
                box_score_parser(bs_url, season_year, playoffs)
    else:
        print("Bad Season url: " + season_url)


if __name__ == "__main__":
    main()