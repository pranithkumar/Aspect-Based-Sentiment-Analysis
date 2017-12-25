from flask import Flask, render_template, redirect, url_for, request
import requests
import json
import ast

app = Flask(__name__, template_folder='.')


@app.route('/test',methods = ['POST', 'GET'])
def login():
     user = request.args.get('nm')
     return redirect(url_for('success',name = user))

@app.route('/success/<name>')
def success(name):
	params = {
  	"api_key": "t3vujAq8hAiM",
  	"start_template": "main_template",
  	"start_value_override": "{\"query\": \"%s\"}" %name,
  	"send_email": "1"
	}
	rp = requests.post("https://www.parsehub.com/api/v2/projects/tBL3WgTTr4aA/run", data=params)

	params = {
  	"api_key": "t3vujAq8hAiM"
	}
	while True:
		rd = requests.get('https://www.parsehub.com/api/v2/runs/'+rp.text[15:27], params=params)
		res=rd.text.split(',')
		ans="{"+res[-2]+"}"
		pages=ast.literal_eval(ans)
		print rp.text[15:27]+" scraped "+str(pages['pages'])+" pages"
		if pages['pages'] >= 6 :
			rc = requests.post("https://www.parsehub.com/api/v2/runs/"+rp.text[15:27]+"/cancel", data=params)
			break
	params = {
  	"api_key": "t3vujAq8hAiM",
  	"format": "json"
	}
	scrape = requests.get("https://www.parsehub.com/api/v2/runs/"+str(rp.text[15:27])+"/data", params=params)
	print scrape.text
	return render_template('review.html', Reviews=json.loads(scrape.text)['Reviews'])
	return "%s" % scrape.text

@app.route('/')
def homepage():
  #params = {'api_key': 'tM_Xm292PTiu',
  #}
  #r = requests.get('https://www.parsehub.com/api/v2/projects/tuZS-MkXJjo0/last_ready_run/data', params=params)
  return render_template('movies.html') #, movies=json.loads(r.text)['movies'])

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
