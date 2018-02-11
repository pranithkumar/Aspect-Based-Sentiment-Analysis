from flask import Flask, render_template, redirect, url_for, request
import requests
import json
import ast
import os
import sys
import time
import os.path

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
    os.system("scrapy crawl searchspiderflipkart")
    f = open('productlinkflipkart.txt','r')
    filenameflipkart = f.read()
    f.close()
    fileflipkart=filenameflipkart.split('/')[1]
    if os.path.exists("data/flipkart/"+fileflipkart+".json"):
        os.system("rm data/flipkart/"+fileflipkart+".json")
    os.system("scrapy crawl completeflipkartscraper -o data/flipkart/"+fileflipkart+".json")
    os.system("scrapy crawl searchspideramazon")
    os.system("scrapy crawl getproductspideramazon")
    f = open('productlinkamazon.txt','r')
    filenameamazon = f.read()
    f.close()
    fileamazon=filenameamazon.split('/')[1]
    if os.path.exists("data/amazon/"+fileamazon+".json"):
        os.system("rm data/amazon/"+fileamazon+".json")
    os.system("scrapy crawl completeamazonscraper -o data/amazon/"+fileamazon+".json")
    return render_template('review.html', AmazonReviews=json.load(open("data/amazon/"+fileamazon+".json")), FlipkartReviews=json.load(open("data/flipkart/"+fileflipkart+".json")))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
