"""
Premier League Data Scraper

This script scrapes a variety of Premier League data from the fbref website.The data will then be
used for analysis, visualization and model training.

Features:
    - [feature]

Usage:
    python scraper.py --season --output

Arguments:
    --season (str): Premier League season to scrape.
    --output (str): File path to save scraped data.

Requirements:
    - selenium
"""
import re
import csv
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


def remove_invalid_rows(stats: list[list[str]]) -> list[list[str]]:
    """Removes invalid rows from team stats."""
    valid_rows = [row for row in stats if len(row) == 20]
    return valid_rows


def add_keys_to_values(stats: list[list[str]], dict_keys: list[str]) -> list[dict[str:str]]:
    """Adds keys to the values and returns the rows as list of dictionaries."""
    stat_dicts = []
    for row in stats:
        new_row = {}
        for i, value in enumerate(row):
            new_row[dict_keys[i]] = value
        stat_dicts.append(new_row)
    return stat_dicts


def get_team_name_from_link(link: str) -> str:
    """Returns the team name from a link."""
    return " ".join(link.split("/")[-1].split("-")[:-1])


def add_team_name_to_rows(stats: list[list[str]], name: str) -> list[dict[str:str]]:
    """Adds the team name to each column."""
    for row in stats:
        row.append(name)
    return stats


def write_stats_to_csv(rows: list[dict[str:str]], headers: list[str], file_path: str) -> None:
    """Writes the team stats to a specified csv file path."""
    with open(file_path, "a", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    args = get_cl_arguments()
    WEBSITE = "https://fbref.com/en/comps/9/2024-2025/2024-2025-Premier-League-Stats"
    column_names = ["date", "time", "comp",
                    "round", "day", "venue",
                    "result", "gf", "ga", "opponent",
                    "xg", "xga", "poss", "attendance",
                    "captain", "formation", "opp_formation",
                    "referee", "match_report", "notes", "team"]
    csv_path = args.output
    team_links = get_team_urls(WEBSITE)
    for team_link in team_links:
        team_stats = get_team_stats(team_link)
        team_stats = remove_invalid_rows(team_stats)
        team_stats = add_team_name_to_rows(
            team_stats, get_team_name_from_link(team_link))
        team_stats = add_keys_to_values(team_stats, column_names)
        write_stats_to_csv(team_stats, column_names, csv_path)
