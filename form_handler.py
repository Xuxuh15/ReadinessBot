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


class Form_Handler:


    def __init__(self,preset):
       load_dotenv()
       self.readiness_preset = preset
       self.driver = webdriver.Chrome()
       self.root = None
       self.name = os.getenv("NAME")
     

    # Launches the web form
    def launch_form(self):
        url = os.getenv("URL")
        self.driver.get(url)
        self.root = self.get_root()

    def get_root(self):
        root =  self.driver.find_elements(By.CSS_SELECTOR, "div.Qr7Oae[role='listitem']")
        print(len(root))
        return root

    # Finds the index of the correct list box from drop down menu
    def find_name(self):
        index = -1 # There is an extra div at the beginning that is skipped by selenium. True index is shifted left by one
        name_boxes = self.driver.find_elements(By.CSS_SELECTOR, "div[jsname='wQNmvb']")
        for name in name_boxes:
            if name.get_attribute("data-value") == self.name:
                return index
            else:
                index += 1
   

    def handle_dropdown_list(self):
        wait = WebDriverWait(self.driver, 10)
        failure_count = 3
        index = self.find_name()
        while failure_count > 0:
            # 1. Open the list box (dropdown)
            list_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[jsname='W85ice']")))
            list_box.click()
            # Prevent blur-triggering interactions by using JS to scroll into view only
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", list_box)
            time.sleep(0.5)  # Wait for the dropdown to fully render
            input_field = self.driver.switch_to.active_element
            for i in range(0, index + 1):
                time.sleep(1)
                if i == index:
                    action = ActionChains(self.driver)
                    action.send_keys(Keys.ARROW_DOWN).pause(0.4).send_keys(Keys.ENTER).perform()
                else:
                    input_field.send_keys(Keys.ARROW_DOWN)
            selected_option = self.driver.find_element(By.CSS_SELECTOR, f"div[data-value='{self.name}']")
            action_successful = selected_option.get_attribute("aria-selected") == 'true'
            print(action_successful)
            if action_successful:
                break
            else:
                failure_count = failure_count - 1
                print(f'Enetered: {failure_count}')



    def handle_sleep_score(self):
        # Sleep Section
        sleep_radio_button = self.root[1].find_element(By.CSS_SELECTOR, f"div[jscontroller='EcW08c'][data-value='{self.readiness_preset['sleep_quality']}']")
        print(f"Sleep Score: {sleep_radio_button.get_attribute('data-value')}")
        sleep_radio_button.click()


    def handle_mood_score(self):
        # Mood Section
        mood_radio_button = self.root[2].find_element(By.CSS_SELECTOR, f"div[jscontroller='EcW08c'][data-value='{self.readiness_preset['mood']}']")
        print(f"Mood Score: {mood_radio_button.get_attribute('data-value')}")
        mood_radio_button.click()

    def handle_soreness_score(self):
        # Soreness Section
        soreness_radio_button = self.root[3].find_element(By.CSS_SELECTOR, f"div[jscontroller='EcW08c'][data-value='{self.readiness_preset['soreness']}']")
        print(f"Soreness Score: {soreness_radio_button.get_attribute('data-value')}")
        soreness_radio_button.click()

    def handle_energy_score(self):
        # Energy Section
        energy_radio_button = self.root[4].find_element(By.CSS_SELECTOR, f"div[jscontroller='EcW08c'][data-value='{self.readiness_preset['energy']}']")
        print(f"Energy Score: {energy_radio_button.get_attribute('data-value')}")
        energy_radio_button.click()

    def handle_performance_score(self):
        # Performance Section
        performance_radio_button = self.root[5].find_element(By.CSS_SELECTOR, f"div[jscontroller='EcW08c'][data-value='{self.readiness_preset['performance']}']")
        print(f"Performance Score: {performance_radio_button.get_attribute('data-value')}")
        performance_radio_button.click()


    def handle_muscle_groups(self):
        muscle_groups = self.readiness_preset['muscle_groups']

        # Build XPath with OR for data-answer-value attributes
        xpath_expr = " or ".join([f"@data-answer-value='{part}'" for part in muscle_groups])

        # Select any element with matching data-answer-value attribute
        full_xpath = f"//*[{xpath_expr}]"

        # Find matching elements
        elements = self.root[6].find_elements(By.XPATH, full_xpath)
        # Filter visible and interact
        for el in elements:
            if el.is_displayed():
                print(el.get_attribute("data-answer-value"))
                el.click()

    def handle_comment_section(self):
        #Fill in the comment section
        comment_field = self.root[7].find_element(By.CSS_SELECTOR, f"input[jsname='YPqjbf']")
        comment_field.send_keys(f"{self.readiness_preset['comment']}")
        print(f"Comment Field: {comment_field.get_attribute('value')}")

    def submit_form(self):
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "div[role='button'][jsname='M2UYVd']")
        submit_button.click()


    def exit_driver(self):
        self.driver.quit()










