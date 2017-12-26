import requests

params = {
  "api_key": "t3vujAq8hAiM"
}
r = requests.get('https://www.parsehub.com/api/v2/runs/tTRuocug2XMX', params=params)
print(r.text)
