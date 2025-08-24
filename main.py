""""Script to scrape match data from the premier league website."""

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd


def get_match_cards(season: int, match_week: int) -> dict[str, list[str]]:
    """Returns a dictionary of match data for a season and week."""
    driver = webdriver.Chrome()
    url = "https://www.premierleague.com" \
        f"/en/matches?competition=8&season={season}&matchweek={match_week}"
    driver.get(url)
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


def create_csv_file(file_path: str):
    """Creates a new empty csv file."""
    new_csv_df = pd.DataFrame(
        columns=["season", "match_week", "home_team", "away_team", "score"])
    new_csv_df.to_csv(path_or_buf=file_path)


if __name__ == "__main__":
    if not file_exists("premier_league_data.csv"):
        create_csv_file("premier_league_data.csv")
    for year in range(2012, 2025):
        for week in range(1, 39):
            match_cards = get_match_cards(year, week)
            match_cards_df = pd.DataFrame(match_cards)
            match_cards_df.to_csv(
                path_or_buf="premier_league_data.csv", mode="a", header=False)
            sleep(1)
