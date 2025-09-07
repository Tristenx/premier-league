"""
Premier League Data Scraper

This script scrapes a variety of Premier League data from the fbref website.The data will then be
used for analysis, visualization and model training.

Features:
    - [feature]

Usage:
    python scraper.py

Arguments:
    --season (str): Premier League season to scrape.
    --output (str): File path to save scraped data.

Requirements:
    - selenium
"""
import re
from argparse import ArgumentParser, Namespace

from selenium import webdriver
from selenium.webdriver.common.by import By


def get_cl_arguments() -> Namespace:
    """Returns a Namespace that contains command-line arguments."""
    parser = ArgumentParser()
    parser.add_argument("season", type=str,
                        help="Premier League season to scrape.")
    parser.add_argument("output", type=str,
                        help="File path to save scraped data.")
    arguments = parser.parse_args()
    return arguments


def get_team_urls(url: str) -> list[str]:
    """Returns links for each teams statistics."""
    driver = webdriver.Chrome()
    driver.get(url)
    table = driver.find_element(By.ID, "switcher_results2024-202591")
    link_elements = table.find_elements(By.TAG_NAME, "a")
    team_urls = list({element.get_attribute("href") for element in link_elements if re.search(
        r"Stats$", element.get_attribute("href"))})
    driver.close()
    return team_urls


def get_team_stats(url: str) -> list[list[str]]:
    """Returns rows from the team statistics table."""
    driver = webdriver.Chrome()
    driver.get(url)
    table = driver.find_element(
        By.ID, "all_matchlogs")
    rows = table.find_elements(By.TAG_NAME, "tr")
    row_values = []
    for row in rows:
        new_row = []
        date = row.find_element(By.TAG_NAME, "th").text
        new_row.append(date)
        values = row.find_elements(By.TAG_NAME, "td")
        for value in values:
            new_row.append(value.text)
        row_values.append(new_row)
    driver.close()
    return row_values


if __name__ == "__main__":
    args = get_cl_arguments()
    WEBSITE = "https://fbref.com/en/comps/9/2024-2025/2024-2025-Premier-League-Stats"
    team_links = get_team_urls(WEBSITE)
    team_stats = get_team_stats(team_links[0])
    print(team_stats)
