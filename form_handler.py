import time
import sys
import os
from datetime import datetime, timezone
from presets import presets
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv


readiness_preset ={}

chrome_options = Options()

# Set the user data directory to your Chrome user data folder
#chrome_options.add_argument("--user-data-dir=/Users/xuxuh/Library/Application Support/Google/Chrome")

# Set the profile directory to the specific profile you want to use (Default, Profile 1, etc.)
#chrome_options.add_argument("--profile-directory=Profile 3")

#driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome()

url = os.getenv("URL")
driver.get(url)



def get_root():
    root = driver.find_elements(By.CSS_SELECTOR, "div.Qr7Oae")
    return root
        
# Selenium will launch chrome with your default profile
root = get_root()   

if root == None:
    sys.exit(3)



def handle_dropdown_list():
    wait = WebDriverWait(driver, 10)
    failure_count = 3
    while failure_count > 0:
        # 1. Open the list box (dropdown)
        list_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[jsname='W85ice']")))
        list_box.click()
        # Prevent blur-triggering interactions by using JS to scroll into view only
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", list_box)
        time.sleep(0.5)  # Wait for the dropdown to fully render
        input_field = driver.switch_to.active_element
        for i in range(0,7):
            time.sleep(1)
            if i == 6:
                action = ActionChains(driver)
                action.send_keys(Keys.ARROW_DOWN).pause(0.4).send_keys(Keys.ENTER).perform()
            else:
                input_field.send_keys(Keys.ARROW_DOWN)
        # Check if the list box option was actually selected. Sometimes it doesn't work on the first try. 
        selected_option = driver.find_element(By.CSS_SELECTOR, "div[data-value='John Hilton']")
        action_successful = selected_option.get_attribute("aria-selected") == 'true'
        print(action_successful)
        if action_successful:
            break
        else:
            failure_count = failure_count - 1
            print(f'Tries Remaining: {failure_count}')



def handle_sleep_score():
    # Sleep Section
    sleep_radio_button = root[1].find_element(By.CSS_SELECTOR, f"div[jscontroller='EcW08c'][data-value='{readiness_preset['sleep_quality']}']")
    print(f"Sleep Score: {sleep_radio_button.get_attribute('data-value')}")
    sleep_radio_button.click()


def handle_mood_score():
    # Mood Section
    mood_radio_button = root[2].find_element(By.CSS_SELECTOR, f"div[jscontroller='EcW08c'][data-value='{readiness_preset['mood']}']")
    print(f"Mood Score: {mood_radio_button.get_attribute('data-value')}")
    mood_radio_button.click()

def handle_soreness_score():
    # Soreness Section
    soreness_radio_button = root[3].find_element(By.CSS_SELECTOR, f"div[jscontroller='EcW08c'][data-value='{readiness_preset['soreness']}']")
    print(f"Soreness Score: {soreness_radio_button.get_attribute('data-value')}")
    soreness_radio_button.click()

def handle_energy_score():
    # Energy Section
    energy_radio_button = root[4].find_element(By.CSS_SELECTOR, f"div[jscontroller='EcW08c'][data-value='{readiness_preset['energy']}']")
    print(f"Energy Score: {energy_radio_button.get_attribute('data-value')}")
    energy_radio_button.click()

def handle_performance_score():
    # Performance Section
    performance_radio_button = root[5].find_element(By.CSS_SELECTOR, f"div[jscontroller='EcW08c'][data-value='{readiness_preset['performance']}']")
    print(f"Performance Score: {performance_radio_button.get_attribute('data-value')}")
    performance_radio_button.click()


def handle_muscle_groups():
    muscle_groups = readiness_preset['muscle_groups']

    # Build XPath with OR for data-answer-value attributes
    xpath_expr = " or ".join([f"@data-answer-value='{part}'" for part in muscle_groups])

    # Select any element with matching data-answer-value attribute
    full_xpath = f"//*[{xpath_expr}]"

    # Find matching elements
    elements = root[6].find_elements(By.XPATH, full_xpath)
    # Filter visible and interact
    for el in elements:
        if el.is_displayed():
            print(el.get_attribute("data-answer-value"))
            el.click()

def handle_comment_section():
    #Fill in the comment section
    comment_field = root[7].find_element(By.CSS_SELECTOR, f"input[jsname='YPqjbf']")
    comment_field.send_keys(f"{readiness_preset['comment']}")
    print(f"Comment Field: {comment_field.get_attribute('value')}")

def submit_form():
    submit_button = driver.find_element(By.CSS_SELECTOR, "div[role='button'][jsname='M2UYVd']")
    submit_button.click()


def exit_driver():
    driver.quit()










