import requests
import os

YOUR_API_KEY = os.environ['mailgun_secret_api']
print(YOUR_API_KEY)

def send_simple_message():
    email = requests.post(
        "https://api.mailgun.net/v3/frmrsmrkt.com/messages",
        auth=("api", YOUR_API_KEY),
        data={"from": "FrmrsMrkt.com <info@frmrsmrkt.com>",
              "to": ["dhcrain@gmail.com", "davis@dhcrain.com"],
              "subject": "Hello",
              "text": "Heeeeeyyyyyyyyyy!!!!!!!")
    print(email)
    return email

send_simple_message()
