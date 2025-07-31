import os
from dotenv import load_dotenv
from twilio.rest import Client




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
    def get_client():
        # Load credentials from environment or .env
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        client = Client(account_sid, auth_token)
        return client

    # Returns the phone number stored in .env file.
    def get_phone_number():
        phone_number = os.getenv("TWILIO_PHONE_NUMBER")
        return phone_number

    # Returns list of x most recent outbound messages. 
    def get_messages(self, x:int):
        messages = self.client.messages.list(to=self.phone_number, limit=x)  # Replace with your recipient number
        return messages
    
    # Returns your phone number stored in .env file.
    def get_my_phone_number():
        phone_number = os.getenv("MY_PHONE_NUMBER")
        return phone_number
    
    # Sends a message to your phone number.
    def send_message(self, msg:str):
        self.client.messages.create(
            body=f"{msg}",
            from_=self.phone_number,
            to=self.my_phone_number
        )
        




