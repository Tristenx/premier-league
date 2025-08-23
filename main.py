""""Script to scrape match data from the premier league website."""

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import pandas as pd


def get_match_cards(season: int, match_week: int) -> list[dict]:
    """Returns a list of match cards for a season and match week."""
    driver = webdriver.Chrome()
    url = f"https://www.premierleague.com/en/matches?competition=8&season={season}&matchweek={match_week}"
    driver.get(url)
    match_container = driver.find_element(
        By.CLASS_NAME, "match-list-root__content")
    match_card_elements = match_container.find_elements(
        By.CLASS_NAME, "match-card__info")

    cards = []
    for element in match_card_elements:
        new_card = {}
        teams = element.find_elements(By.CLASS_NAME,
                                      "match-card__team-name-container")
        new_card["home_team"] = teams[0].text
        new_card["away_team"] = teams[1].text
        new_card["score"] = element.find_element(
            By.CLASS_NAME, "match-card__score").text
        cards.append(new_card)

    driver.close()
    return cards


if __name__ == "__main__":
    match_cards = get_match_cards(2025, 1)
    print(match_cards)
