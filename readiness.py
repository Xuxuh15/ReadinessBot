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
from twilio_client import User
from form_runner import FormRunner


def execute_readiness_bot():
    client = User()

    readiness_preset = client.get_todays_code(presets)

    form_runner = FormRunner(readiness_preset)

    form_runner.run()

    if form_runner.successful:
        client.send_message(f"{form_runner.message} at timestamp: {timezone.utc}")
    else:
        client.send_message(f"Submission Failed: {form_runner.message} at timestamp: {timezone.utc}")


execute_readiness_bot()













