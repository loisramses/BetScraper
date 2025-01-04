import requests

bot_token = "8049483033:AAFVQhsU1luOWGPPY7SC3INAfd2khpHAV9Q"
chat_id = "1399479471"
message = "nigger"

url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
payload = {"chat_id": chat_id, "text": message}
response = requests.post(url, json=payload)

if response.status_code == 200:
    print("OK")
else:
    print("NOK")