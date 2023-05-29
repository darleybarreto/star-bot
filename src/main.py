import time
import argparse
from sys import exit
from datetime import datetime

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
                    prog='Star Bot',
                    description="Scrape data from Estrela Bet's website")

    parser.add_argument('team')
    parser.add_argument("-t", "--timeout",
                        default=5,
                        type=int,
                        help="Timeout to wait for Chromium webengine load website.")
    args = parser.parse_args()
    team = args.team.lower()

    driver = webdriver.Chrome(options=set_chrome_options())
    driver.get(URL.format(team))

    css_selector = "#container-main > app-fixture-search > div.srch.page > div.modul-accordion.sportType > div.modul-content"
    time.sleep(10)

    try:
        el = driver.find_element(By.CSS_SELECTOR, css_selector)
    except:
        print("No games found or timeout needs to be increased")
        exit(1)

    leagues = el.find_elements(By.XPATH,"*")
    
    odds_dict = {}

    for i,l in enumerate(leagues, start=1):
        inner_div_content = l.find_element(By.CSS_SELECTOR,f"div:nth-child({i}) > div.modul-content > div")
        inner_elements = inner_div_content.find_elements(By.XPATH,"*")

        if len(inner_elements) == 0:
            continue

        date_str = inner_elements[1].text.rstrip().strip().split()[-1]
        date = datetime.strptime(date_str, '%d/%m/%Y')
        
        columns = inner_elements[2].text.split("\n")
        index = [i for i, e in enumerate(columns) if e == args.team][-1]
        odds_dict[date] = float(columns[index - 1])

    if len(odds_dict) == 0:
        print("No games found")
    else:
        sorted_dates = sorted(odds_dict)
        next_date = sorted_dates[0]
        odds = odds_dict[next_date]
        pprint_date = next_date.strftime("%d/%m/%Y")
        print(f"The odds of {args.team} winning the next game on {pprint_date} are {odds}")
    
    driver.close()

if __name__ == "__main__":
    main()