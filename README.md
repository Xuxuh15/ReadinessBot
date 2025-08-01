# Readinessbot 🤖📋

**Automates a daily readiness check-in with a simple emoji**

`readinessbot` is a personal automation script that uses **Selenium** and **Twilio** to fill out a daily Google readiness form for based on a quick text message you send each morning.

## 🚀 What It Does

- Runs automatically as a background process on your Mac each morning.
- Waits for a text from you in the format:  
  `emoji:[body parts]:comment`  
  Example: `💪:shoulders,ankles,arms:feeling good overall`  
  Or just: `💪` for a quick preset.
- Maps the emoji to a predefined readiness preset from `presets.py`.
- Fills out the Google Form with the appropriate values using Selenium.
- Sends you a status update via text once the form has been successfully submitted.
- Includes a timeout to avoid running indefinitely, polling your texts every 5 minutes.

## 🧠 How It Works

1. **Presets**: You define emojis and corresponding form values in `presets.py`.
2. **Trigger**: A background job launches each morning at a preset time.
3. **Polling**: The script checks your text messages every 5 minutes (via Twilio) for input.
4. **Form Submission**: Once it gets a valid message, it fills and submits the Google Form.
5. **Feedback**: You receive a confirmation text so you know you're all set.

## 📂 File Structure

```
readinessbot/
├── readiness.py # executes the form_runner and texts results to user
├── presets.py # Your custom emoji-to-form presets
├── form_handler.py # Selenium logic to interact with the Google Form
|── form_runner.py # executes the form handler methods in order and handles exceptions
├── twilio_client.py # Handles SMS send/receive with Twilio
├── .env # Configuration values (e.g. timeout, polling interval)
└── README.md # This file
```

## ✅ Requirements

- Python 3.7+
- Selenium
- Twilio Python SDK
- ChromeDriver (or other compatible WebDriver)
- A Twilio account with an active phone number
- macOS (for background launch scheduling)

## 🛠 Setup

1. **Install dependencies**:

```bash
pip install selenium twilio
```
2. Set up your environment variables for Twilio credentials and form URL.

3. Configure your presets in presets.py.

4. Schedule the script using launchd, cron, or a background job manager like pm2.

## 💬 Example Preset (in presets.py)

```python

PRESETS = {
    "💪": {
        "energy": "High",
        "mood": "Great",
        "soreness": "Shoulders",
        "comment": "Ready to crush it!"
    },
    "😴": {
        "energy": "Low",
        "mood": "Tired",
        "soreness": "Legs",
        "comment": "Rough night"
    }
}
```
## 📩 SMS Format
emoji:[muscle groups]:comment

Parts after the emoji are optional and will override the preset values.

Example: 😴::Still waking up will use the 😴 preset but override only the comment.

## ⏰ Timeout Behavior
If no message is received within a configurable timeout window (e.g. 30 minutes), the script will stop polling to avoid running indefinitely.

## 📬 Status Updates
After submitting the form, the script will send you a confirmation SMS so you know the task was completed or update you in case of a failure.
