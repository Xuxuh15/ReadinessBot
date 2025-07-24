from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()

# Set the user data directory to your Chrome user data folder
#chrome_options.add_argument("--user-data-dir=/Users/xuxuh/Library/Application Support/Google/Chrome")

# Set the profile directory to the specific profile you want to use (Default, Profile 1, etc.)
#chrome_options.add_argument("--profile-directory=Profile 3")

#driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome()

driver.get("https://docs.google.com/forms/d/e/1FAIpQLSdhcHRqJx-SB1-mhr8mJ6yStqDSgt2XeP0sqWwe-_j8vrh5ZA/viewform")

# Now Selenium will open Chrome with your profile, keeping your logged-in session\

name = "<input type='hidden' name='entry.584514674' value='John Hilton'>"
comment = "<input type='hidden' name='entry.965250582' value='hello'>"
sleep = "<input type='hidden' name='entry.1340191238' value='1'>"
soreness = "<input type='hidden' name='entry.1160513184' value='1'>"
mood = "<input type='hidden' name='entry.850635128' value='1'>"
energy = "<input type='hidden' name='entry.850635128' value='1'>"
performance = "<input type='hidden' name='entry.24355936' value='1'>"
body_group = "<input type='hidden' name='entry.1475504717' value='Head'>"





name = 'John Hilton'
sleep_score = 7
soreness_score = 7
mood_score = 7
energy_score = 7
performance_score = 6
body_group_selection = 'ankle'
comment = ''



children1 = driver.find_elements(By.CSS_SELECTOR, "div.Qr7Oae")
print(len(children1))

option = driver.find_element(By.CSS_SELECTOR, "div[data-value='John Hilton']")
driver.execute_script("arguments[0].click();", option)


sleep_radio_button = children1[1].find_element(By.CSS_SELECTOR, f"div[jscontroller='EcW08c'][data-value='{sleep_score}']")
print(f"Sleep Score: {sleep_radio_button.get_attribute('data-value')}")
sleep_radio_button.click()

mood_radio_button = children1[2].find_element(By.CSS_SELECTOR, f"div[jscontroller='EcW08c'][data-value='{mood_score}']")
print(f"Mood Score: {mood_radio_button.get_attribute('data-value')}")
mood_radio_button.click()

soreness_radio_button = children1[3].find_element(By.CSS_SELECTOR, f"div[jscontroller='EcW08c'][data-value='{soreness_score}']")
print(f"Soreness Score: {soreness_radio_button.get_attribute('data-value')}")
soreness_radio_button.click()

energy_radio_button = children1[4].find_element(By.CSS_SELECTOR, f"div[jscontroller='EcW08c'][data-value='{energy_score}']")
print(f"Energy Score: {energy_radio_button.get_attribute('data-value')}")
energy_radio_button.click()

performance_radio_button = children1[5].find_element(By.CSS_SELECTOR, f"div[jscontroller='EcW08c'][data-value='{performance_score}']")
print(f"Performance Score: {energy_radio_button.get_attribute('data-value')}")
performance_radio_button.click()





body_parts = ["Head", "Legs", "Arms"]  # your target strings

# Build XPath with OR for data-answer-value attributes
xpath_expr = " or ".join([f"@data-answer-value='{part}'" for part in body_parts])

# Select any element with matching data-answer-value attribute
full_xpath = f"//*[{xpath_expr}]"

# Find matching elements
elements = children1[6].find_elements(By.XPATH, full_xpath)
# Filter visible and interact
for el in elements:
    if el.is_displayed():
        print(el.get_attribute("data-answer-value"))
        el.click()





          




list_item = driver.find_element(By.CSS_SELECTOR, "input[type='hidden']")
print(list_item)
print(list_item.tag_name)
children = driver.find_elements(By.CSS_SELECTOR, "div.child-class")


print(len(children))









