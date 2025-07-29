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
from twilio.rest import Client



name = os.getenv("NAME")
sleep_score = 7
soreness_score = 7
mood_score = 7
energy_score = 7
performance_score = 6
muscle_groups = ["Ankles"]  
comment = 'This was written by a bot (╯°□°）╯︵ ┻━┻'


load_dotenv()

# Load credentials from environment or .env
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
phone_number = os.getenv("TWILIO_PHONE_NUMBER")
client = Client(account_sid, auth_token)

# Get recent sent messages
messages = client.messages.list(to=phone_number, limit=2)  # Replace with your recipient number
today = datetime.now(timezone.utc).date()

readiness_preset = None
start_time = time.time()
msg_received = False
message = None
timeout = 1300
# Wait for a readiness message to be sent in the morning
while not msg_received:

    elapsed = time.time() - start_time
    if elapsed > timeout:
        readiness_preset = presets['👌']
        msg_received = True
        break
    try:
        message = client.messages.list(limit=3)
        print(message)
        for msg in message:
            print(msg.direction)
            if msg.direction.startswith("inbound") and msg.date_sent.date() == today:
                unicode = msg.body.strip()
                readiness_preset = presets[unicode]
                msg_received = True
                break
    except Exception as e:
        pass
    if not msg_received:
          time.sleep(300)  # check every 5 minutes if no message recceived
  

chrome_options = Options()

# Set the user data directory to your Chrome user data folder
#chrome_options.add_argument("--user-data-dir=/Users/xuxuh/Library/Application Support/Google/Chrome")

# Set the profile directory to the specific profile you want to use (Default, Profile 1, etc.)
#chrome_options.add_argument("--profile-directory=Profile 3")

#driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome()

url = os.getenv("URL")
driver.get(url)

# Selenium will launch chrome with your default profile
root = None 

try:
    root = driver.find_elements(By.CSS_SELECTOR, "div.Qr7Oae")
    if len(root) != 8 :
        sys.exit(4)
except Exception as e:
    sys.exit(3)


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
    selected_option = driver.find_element(By.CSS_SELECTOR, "div[data-value='John Hilton']")
    action_successful = selected_option.get_attribute("aria-selected") == 'true'
    print(action_successful)
    if action_successful:
        break
    else:
        failure_count = failure_count - 1
        print(f'Enetered: {failure_count}')





# Sleep Section
sleep_radio_button = root[1].find_element(By.CSS_SELECTOR, f"div[jscontroller='EcW08c'][data-value='{sleep_score}']")
print(f"Sleep Score: {sleep_radio_button.get_attribute('data-value')}")
sleep_radio_button.click()

# Mood Section
mood_radio_button = root[2].find_element(By.CSS_SELECTOR, f"div[jscontroller='EcW08c'][data-value='{mood_score}']")
print(f"Mood Score: {mood_radio_button.get_attribute('data-value')}")
mood_radio_button.click()

# Soreness Section
soreness_radio_button = root[3].find_element(By.CSS_SELECTOR, f"div[jscontroller='EcW08c'][data-value='{soreness_score}']")
print(f"Soreness Score: {soreness_radio_button.get_attribute('data-value')}")
soreness_radio_button.click()

# Energy Section
energy_radio_button = root[4].find_element(By.CSS_SELECTOR, f"div[jscontroller='EcW08c'][data-value='{energy_score}']")
print(f"Energy Score: {energy_radio_button.get_attribute('data-value')}")
energy_radio_button.click()

# Performance Section
performance_radio_button = root[5].find_element(By.CSS_SELECTOR, f"div[jscontroller='EcW08c'][data-value='{performance_score}']")
print(f"Performance Score: {energy_radio_button.get_attribute('data-value')}")
performance_radio_button.click()


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


#Fill in the comment section
comment_field = root[7].find_element(By.CSS_SELECTOR, f"input[jsname='YPqjbf']")
print(comment_field.tag_name)
comment_field.send_keys(comment)
print(f"Comment Field: {comment_field.get_attribute('value')}")


#submit_button = driver.find_element(By.CSS_SELECTOR, "div[role='button'][jsname='M2UYVd']")
#submit_button.click()

input("Press Enter to close the browser...")  # wait until I press enter
driver.quit()













