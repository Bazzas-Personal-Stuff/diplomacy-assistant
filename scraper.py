from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os

load_dotenv()
WD_GAME_ID = os.getenv('WD_GAME_ID')
ROOT_URL = "https://webdiplomacy.net/"
GAME_URL = ROOT_URL + "board.php?gameID="

soup: any


def get_soup():
    global soup
    response = requests.get(GAME_URL + str(WD_GAME_ID))
    text = response.text
    soup = BeautifulSoup(text, 'html.parser')


def get_date_and_phase() -> (str, str, str):
    get_soup()
    season_and_year: list = soup.find("span", class_="gameDate").string.strip().split(", ")
    season = season_and_year[0]
    year = season_and_year[1]
    phase: str = soup.find("span", class_="gamePhase").string
    return season, year, phase


def get_map_url() -> str:
    map_link = soup.find(id='LargeMapLink')
    return ROOT_URL + map_link['href']
