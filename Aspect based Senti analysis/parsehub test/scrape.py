import requests

params = {
  "api_key": "t3vujAq8hAiM",
  "format": "json"
}
r = requests.get('https://www.parsehub.com/api/v2/runs/tTiri_e-GQuC/data', params=params)
print(r.text)