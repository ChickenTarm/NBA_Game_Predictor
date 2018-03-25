import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime


class Game_Player(object):

    def __init__(self, name):
        self.name = name



def box_score_parser(url):
    bs_resp = requests.get(url)

    if bs_resp.ok:
        bs_parser = BeautifulSoup(bs_resp.text, "html.parser")

        headline = bs_parser.find_all('h1')[0].get_text()

        date_start = headline.find(', ')

        date = datetime.strptime(headline[date_start + 2:], "%B %d, %Y")

        if date.month > 8:
            season = date.year + 1
        else:
            season = date.year

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
        game["home_score"] = home_pts
        game["away_score"] = away_pts

        game["home"] = home_team
        game["away"] = away_team

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

    json.dump(game, open("../data/nba/" + str(season) + "/" + url[last_slash + 1:-5] + ".json", 'w'), indent=4)



def main():

    url = "https://www.basketball-reference.com/boxscores/201611010CLE.html"

    box_score_parser(url)



if __name__ == "__main__":
    main()