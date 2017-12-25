import requests

params = {
  "api_key": "t3vujAq8hAiM",
  "start_template": "main_template",
  "start_value_override": "{\"query\": \"vivo v7\"}",
  "send_email": "1"
}
r = requests.post("https://www.parsehub.com/api/v2/projects/tBL3WgTTr4aA/run", data=params)

print(r.text[15:27])

