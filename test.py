import requests

bot_token = "8049483033:AAFVQhsU1luOWGPPY7SC3INAfd2khpHAV9Q"
chat_id = "1399479471"
message = """
*Oportunidade*
*TSV Hartberg : UVC Graz*
*Tipo de aposta:* Vencedor
*1ª opção:* [UVC Graz](https://www.casinoportugal.pt/desportos/mercados/1234489) *Odd:* 2\\.47
*2ª opção:* [TSV Hartberg \\(F\\)](https://www.betano.pt/odds/tsv-hartberg-f-uvc-graz-f/60961514/) *Odd:* 4\\.75
*Percentagem:* 38\\.46153846153846
*Taxa de confiança:* 92\\.5925925925926
"""

url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
payload = {"chat_id": chat_id, "text": message, "parse_mode": "MarkdownV2", "link_preview_options": {"is_disabled": True}}
response = requests.post(url, json=payload)

if response.status_code == 200:
    print("OK")
else:
    print("NOK")
    print(response.content)
