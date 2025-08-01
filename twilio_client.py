import os
import time
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.rest.api.v2010.account.message import MessageInstance
from datetime import datetime, timezone
from presets import presets




class User:


    def __init__(self):
        try:
            load_dotenv()
            self.phone_number = self.get_phone_number()
            self.client = self.get_client()
            self.my_phone_number = self.get_my_phone_number()
        except Exception as e:
            print("Error authenticating user. Check .env variables and try again.")

    # Returns a Twilio client instance. Authenticating info should be stored in .env file.
    def get_client(self):
        # Load credentials from environment or .env
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        client = Client(account_sid, auth_token)
        return client

    # Returns the phone number stored in .env file.
    def get_phone_number(self):
        phone_number = os.getenv("TWILIO_PHONE_NUMBER")
        return phone_number

    # Returns list of x most recent inbound messages. 
    def get_messages(self, x:int):
        messages = self.client.messages.list(from_=self.my_phone_number, limit=x)  # Replace with your recipient number
        return messages
    
    # Returns your phone number stored in .env file.
    def get_my_phone_number(self):
        phone_number = os.getenv("MY_PHONE_NUMBER")
        return phone_number
    
    # Sends a message to your phone number.
    def send_message(self, msg:str):
        self.client.messages.create(
            body=f"{msg}",
            from_=self.phone_number,
            to=self.my_phone_number
        )

    # Extracts readiness_preset from inbound text message
    def get_readiness_preset(self,msg:MessageInstance):
        print(msg)
        sections = msg.body.split(":")
        unicode = sections[0].strip()
        try:
            readiness_preset = presets[unicode]
            if(len(sections) > 1):
                muscle_groups = sections[1].split((","))
                muscle_groups= [muscle.capitalize() for muscle in muscle_groups]
                readiness_preset['muscle_groups'] = muscle_groups
            if(len(sections) > 2):
                comment = sections[2]
                readiness_preset['comment'] = comment
            return readiness_preset
        except KeyError:
            return None
           

    # gets the readiness score for today {sent as a text message by user}
    def get_todays_code(self, presets):
        # Get recent sent messages
        messages = self.get_messages(3)
        today = datetime.now(timezone.utc).date()

        readiness_preset = None
        start_time = time.time()
        msg_received = False
        timeout = 1300
        # Wait for a readiness message to be sent in the morning
        while not msg_received:

            elapsed = time.time() - start_time # current time elapsed
            if elapsed > timeout: # if the elapsed time exxceeds the timeout, we exit the function with a default preset
                readiness_preset = presets['👌']
                msg_received = True
                break
            try:
                for msg in messages:
                    if msg.direction.startswith("inbound") and msg.date_sent.date() == today:
                        readiness_preset = self.get_readiness_preset(msg)
                        if readiness_preset:
                              msg_received = True
                              break
            except Exception as e:
                print('Exception raised at msg_received')
                pass
            if not msg_received:
                time.sleep(300)  # poll twilio api for a message every 5 minutes
        return readiness_preset
   




