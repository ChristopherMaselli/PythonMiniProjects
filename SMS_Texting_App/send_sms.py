from twilio.rest import Client  # Importing Twilio's rest framework
# Pulling credentials from the credentials file to make them available here
from credentials import account_sid, auth_token, my_cell, my_twilio

client = Client(account_sid, auth_token)

my_msg = "".join(['Hi there!\n' for i in range(100)])

message = client.messages.create(
    from_=my_twilio, to=my_cell, body=my_msg)

print(message.sid)
