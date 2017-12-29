import requests

params = {
  "api_key": "t3vujAq8hAiM"
}
r = requests.get('https://www.parsehub.com/api/v2/runs/tTiri_e-GQuC', params=params)
print(r.text)
