import requests
from bs4 import BeautifulSoup


def main():

    url = "https://www.basketball-reference.com/boxscores/201611010CLE.html"

    resp = requests.get(url)

    if resp.ok:
        parser = BeautifulSoup(resp.text, "html.parser")
        print(parser.prettify())
    else:
        print("Bad url: " + url)


if __name__ == "__main__":
    main()