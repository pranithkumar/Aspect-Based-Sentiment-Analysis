import requests

params = {
  "api_key": "t3vujAq8hAiM"
}
r = requests.post("https://www.parsehub.com/api/v2/runs/tegmCPGwivD9/cancel", data=params)

print(r.text)

