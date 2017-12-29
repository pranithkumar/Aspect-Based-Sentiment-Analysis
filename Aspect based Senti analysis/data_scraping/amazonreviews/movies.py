from flask import Flask, render_template, redirect, url_for, request
import requests
import json
import ast
import os
import sys

app = Flask(__name__, template_folder='.')

@app.route('/')
def homepage():
    return render_template('movies.html')

@app.route('/test',methods = ['POST', 'GET'])
def login():
    user = request.args.get('nm')
    return redirect(url_for('success',name = user))

@app.route('/success/<name>')
def success(name):
    f = open('input.txt','w')
    f.write(name)
    f.close()
    runf = 'scrapy crawl searchspider'
    os.system(runf)
    runf = 'scrapy crawl getproductspider'
    os.system(runf)
    runf = 'scrapy crawl completeamazonscraper -o amazonreviews.json'
    os.system(runf)
    sys.exit(0)
    return render_template('review.html', Reviews=json.load(open('data.json')))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
