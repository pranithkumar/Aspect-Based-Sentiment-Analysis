from flask import Flask, render_template, redirect, url_for, request
import requests
import json
import ast
import os
import sys
import time

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
    f = open('productlinkamazon.txt','r')
    titlesamazon = f.read()
    f.close()
    titleamazon=titlesamazon.split('/')[1]
    f = open('productlinkflipkart.txt','r')
    titlesflipkart = f.read()
    f.close()
    titleflipkart=titlesflipkart.split('/')[1]
    os.system("scrapy crawl searchspiderflipkart")
    os.system("scrapy crawl completeflipkartscraper -o data/flipkart/"+titleflipkart+".json")
    os.system("scrapy crawl searchspideramazon")
    os.system("scrapy crawl getproductspideramazon")
    os.system("scrapy crawl completeamazonscraper -o data/amazon/"+titleamazon+".json")
    return render_template('review.html', AmazonReviews=json.load(open("data/amazon/"+titleamazon+".json")), FlipkartReviews=json.load(open("data/flipkart/"+titleflipkart+".json")))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
