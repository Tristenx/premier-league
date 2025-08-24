""""Script to scrape match data from the premier league website."""

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import requests as req
from bs4 import BeautifulSoup


def get_match_cards(season: int, match_week: int) -> dict[str, list[str]]:
    """Returns a dictionary of match data for a season and week."""
    driver = webdriver.Chrome()
    url = "https://www.premierleague.com" \
        f"/en/matches?competition=8&season={season}&matchweek={match_week}"
    driver.get(url)
    sleep(1)
    match_container = driver.find_element(
        By.CLASS_NAME, "match-list-root__content")
    match_card_elements = match_container.find_elements(
        By.CLASS_NAME, "match-card__info")

    cards = {"season": [season for i in range(len(match_card_elements))],
             "match_week": [match_week for i in range(len(match_card_elements))],
             "home_team": [i.find_elements(
                 By.CLASS_NAME, "match-card__team-name-container")[0].text
                 for i in match_card_elements],
             "away_team": [i.find_elements(
                 By.CLASS_NAME, "match-card__team-name-container")[1].text
                 for i in match_card_elements],
             "score": [i.find_element(
                 By.CLASS_NAME, "match-card__score").text
                 for i in match_card_elements]}

    driver.close()
    return cards


def file_exists(file_path: str) -> bool:
    """Checks if a file exists and returns a bool."""
    try:
        with open(file=file_path, mode="r", encoding="utf-8") as _:
            pass
        return True
    except FileNotFoundError:
        return False


def create_csv_file(file_path: str) -> None:
    """Creates a new empty csv file."""
    new_csv_df = pd.DataFrame(
        columns=["season", "match_week", "home_team", "away_team", "score"])
    new_csv_df.to_csv(path_or_buf=file_path)


def populate_csv_with_match_cards(file_name) -> None:
    """Populates a csv with match cards."""
    if not file_exists(file_name):
        create_csv_file(file_name)
    for year in range(2012, 2025):
        for week in range(1, 39):
            match_cards = get_match_cards(year, week)
            match_cards_df = pd.DataFrame(match_cards)
            match_cards_df.to_csv(
                path_or_buf=file_name, mode="a", header=False)


def get_team_elo_soup(season: int) -> BeautifulSoup:
    """Returns every team elo for a season"""
    season = f"{season}-{season+1}"
    url = f"https://elofootball.com/country.php?countryiso=ENG&season={season}"
    res = req.get(url, timeout=15)
    if res.status_code == 200:
        return BeautifulSoup(res.text, "html.parser")
    raise req.exceptions.ConnectionError(res.status_code, res.reason)


def get_team_elo(soup: BeautifulSoup) -> dict[str, str]:
    """Extracts team elos from soup."""
    table_contents = list(filter(None, soup.find(
        attrs={"id": "Ranking"}).get_text().split("\n\n")))
    table_contents = table_contents[1:]

    team_stats = {}
    for team in table_contents:
        stats = list(filter(None, team.split("\n")))
        if len(stats) > 3:
            team_name = " ".join(stats[0].split(
                " ")[1:]).replace("FC", "").strip()
            team_elo = stats[7]
            team_stats[team_name] = team_elo
    return team_stats


def fill_home_elo_column(x) -> str:
    """Function used to apply ranking to elo column."""
    rankings = yearly_ratings[x["season"]]
    return rankings.get(x["home_team"])


def fill_away_elo_column(x) -> str:
    """Function used to apply ranking to elo column."""
    rankings = yearly_ratings[x["season"]]
    return rankings.get(x["away_team"])


if __name__ == "__main__":
    populate_csv_with_match_cards("premier_league_data.csv")
    data = pd.read_csv("premier_league_data.csv")
    yearly_ratings = {}
    for year in range(2012, 2025):
        yearly_ratings[year] = get_team_elo(get_team_elo_soup(year))
    data["home_elo"] = data.apply(fill_home_elo_column, axis=1)
    data["away_elo"] = data.apply(fill_away_elo_column, axis=1)
    data.to_csv("premier_league_data.csv")
