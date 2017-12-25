import requests

params = {
  "api_key": "t3vujAq8hAiM"
}
r = requests.post("https://www.parsehub.com/api/v2/runs/tnDbKLBsL_mh/cancel", data=params)

print(r.text)

