from collections import defaultdict as DD
import json

# Selenium is used as specific JavaScript components must be loaded
# Selenium Websdriver Stuff
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
# Extra Selenium Stuff
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# The url takes a single argument "lvl" which is the level of the page you want to scrape
_UNFORMATTED_LEVEL_URL = "https://wordscapessolver.com/?lvl={level}"


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"}

# Any element with this class has text that is an answer
_ANSWER_CLASS = "btn-answer"

def get_chrome_driver(headless=False):
    # This requires that Google Chrome is installed in the default location

    # (on windows)
    # C:\Users%USERNAME%\AppData\Local\Google\Chrome\Application\chrome.exe

    # For Linux systems, the ChromeDriver expects /usr/bin/google-chrome to be a symlink to the actual Chrome binary.
    # More Info Here: https://stackoverflow.com/questions/50138615/webdriverexception-unknown-error-cannot-find-chrome-binary-error-with-selenium
    options = ChromeOptions()

    if headless:
        options.add_argument("--headless")

    return webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))

def get_answers_on_page(driver):
    answer_elements = driver.find_elements(By.CLASS_NAME, _ANSWER_CLASS)

    answer_dict = DD(list)
    for answer_element in answer_elements:
        answer = answer_element.get_attribute("text").strip()
        answer_dict[str(len(answer))].append(answer)

    # Hyjacking the current level from the url
    level = driver.current_url.split("=")[1]
    answers = dict(answer_dict)
    print(f"Found the answers for level {level}: {answers}")

    return {level:answers}

def save_answers(answers):
    print("Saving answers...")

    dbfile = "./database/2000.json" 
    with open(dbfile, "r+") as dumpfile:
        levels = json.load(dumpfile)
        levels.update(answers)
    with open(dbfile, "w") as dumpfile:
        json.dump(levels, dumpfile)

def get_answer_from_level(level):
    driver = get_chrome_driver(headless=True)
    driver.implicitly_wait(5)
    driver.get(_UNFORMATTED_LEVEL_URL.format(level=level))
    return get_answers_on_page(driver)

def get_many_answers_from_levels(first_level=1, last_level=1000):
    driver = get_chrome_driver(headless=True)
    driver.implicitly_wait(5)
    for current_level in range(first_level, last_level+1):
        driver.get(_UNFORMATTED_LEVEL_URL.format(level=current_level))
        answers = get_answers_on_page(driver)
        save_answers(answers)
        # driver.back()

def main():
    get_many_answers_from_levels(first_level=605, last_level=1000)
    # print(get_answers_by_level(209))

if __name__ == "__main__":
    main()