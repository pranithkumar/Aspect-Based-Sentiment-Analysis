import requests

params = {
  "api_key": "t3vujAq8hAiM",
  "offset": "0",
  "limit": "20",
  "include_options": "1"
}
r = requests.get('https://www.parsehub.com/api/v2/projects', params=params)
print(r.text)
