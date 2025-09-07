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

from selenium import webdriver
from selenium.webdriver.common.by import By


def get_team_stat_links(url: str) -> list[str]:
    """Returns links for each teams statistics."""
    driver = webdriver.Chrome()
    driver.get(url)
    table = driver.find_element(By.ID, "switcher_results2024-202591")
    link_elements = table.find_elements(By.TAG_NAME, "a")
    team_links = [element.get_attribute("href") for element in link_elements if re.search(
        "Stats$", element.get_attribute("href"))]
    driver.close()
    return team_links


if __name__ == "__main__":
    WEBSITE = "https://fbref.com/en/comps/9/2024-2025/2024-2025-Premier-League-Stats"
    team_stat_links = get_team_stat_links(WEBSITE)
    print(team_stat_links)
