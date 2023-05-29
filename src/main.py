import time
import argparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

URL = "https://estrelabet.com/ptb/bet/search/{}"

def set_chrome_options() -> Options:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options

def main():
    parser = argparse.ArgumentParser(
                    prog='Estrela Scraper',
                    description="Scrape Estrela Bet's website")

    parser.add_argument('team')
    args = parser.parse_args()
    team = args.team.lower()

    driver = webdriver.Chrome(options=set_chrome_options())
    driver.get(URL.format(team))

    css_selector = "#container-main > app-fixture-search > div.srch.page > div.modul-accordion.sportType"
    
    try:
        time.sleep(5)
        el = driver.find_element(By.CSS_SELECTOR, css_selector)
    except:
        print("No game found")

    children = el.find_elements(By.XPATH,"*")
    games = children[-1].find_elements(By.XPATH,"*")
    
    if len(games) > 0:
        first_game_table = games[0].find_elements(By.XPATH,"*")
        table = first_game_table[-1]\
            .find_element(By.CSS_SELECTOR, "div.fixture-container")\
            .find_elements(By.XPATH, "*")[2]
        columns = table.text.split("\n")
        index = [i for i, e in enumerate(columns) if e == args.team][-1]
        odds = float(columns[index - 1])
        print(f"The odds of {args.team} winning the next game are {odds}")

    else:
        print("No game found")
    
    
    driver.close()

if __name__ == "__main__":
    main()