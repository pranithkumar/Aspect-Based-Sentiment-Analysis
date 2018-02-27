
#This file runs a flask application that scrapes data from amazon and flipkart for specific products by executing scrapy spiders
from flask import Flask, render_template, redirect, url_for, request
import requests
import json
import ast
import os
import sys
import time
import os.path

app = Flask(__name__, template_folder='.')

#defining the homepage
@app.route('/')
def homepage():
    return render_template('movies.html')

#taking the search keyword as input
@app.route('/test',methods = ['POST', 'GET'])
def login():
    user = request.args.get('nm')
    return redirect(url_for('success',name = user))

#function that executes the spiders and stores the output in json files
@app.route('/success/<name>')
def success(name):
    #storing input search keyword in input.txt
    f = open('/home/ubuntu/Aspect-Based-Sentiment-Analysis/Aspect based Senti analysis/data_scraping/reviewscraper/input.txt','w')
    f.write(name)
    f.close()
#    print "step 1"
    os.chdir('/home/ubuntu/Aspect-Based-Sentiment-Analysis/Aspect based Senti analysis/data_scraping/reviewscraper/')
#    print "step 2"
    os.system("scrapy crawl searchspiderflipkart")
#    print "step 3"
    f = open('/home/ubuntu/Aspect-Based-Sentiment-Analysis/Aspect based Senti analysis/data_scraping/reviewscraper/productlinkflipkart.txt','r')
#    print "step 4"
    #extracting filename of the json file to be stored from productlinkflipkart.txt
    filenameflipkart = f.read()
    f.close()
    fileflipkart=filenameflipkart.split('/')[1]
    #check if the file already exists
    if os.path.exists("data/flipkart/"+fileflipkart+".json"):
        os.system("rm data/flipkart/"+fileflipkart+".json")
#    print "step 5"
    os.system("scrapy crawl completeflipkartscraper -o data/flipkart/"+fileflipkart+".json")
#    print "step 6"
    os.system("scrapy crawl searchspideramazon")
#    print "step 7"
    os.system("scrapy crawl getproductspideramazon")
#    print "step 8"
    f = open('/home/ubuntu/Aspect-Based-Sentiment-Analysis/Aspect based Senti analysis/data_scraping/reviewscraper/productlinkamazon.txt','r')
    #extracting filename of the json file to be stored from productlinkamazon.txt
#    print "step 9"
    filenameamazon = f.read()
    f.close()
    fileamazon=filenameamazon.split('/')[1]
    #check if the file already exists
    if os.path.exists("data/amazon/"+fileamazon+".json"):
        os.system("rm data/amazon/"+fileamazon+".json")
#    print "step 10"
    os.system("scrapy crawl completeamazonscraper -o data/amazon/"+fileamazon+".json")
    #rendering data from files to the html output
#    print "step 11"
    return render_template('review.html', AmazonReviews=json.load(open("/home/ubuntu/Aspect-Based-Sentiment-Analysis/Aspect based Senti analysis/data_scraping/reviewscraper/data/amazon/"+fileamazon+".json")), FlipkartReviews=json.load(open("/home/ubuntu/Aspect-Based-Sentiment-Analysis/Aspect based Senti analysis/data_scraping/reviewscraper/data/flipkart/"+fileflipkart+".json")))

if __name__ == '__main__':
#    app.run(host='0.0.0.0', debug=True)
     app.run()
