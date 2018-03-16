#This file runs a flask application that scrapes data from amazon and flipkart for specific products by executing scrapy spiders
from flask import Flask, render_template, redirect, url_for, request
import requests,json,os,sys,time,os.path,ast,string,re
from final_aspect_entity_extraction import *

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

    os.chdir('/home/ubuntu/Aspect-Based-Sentiment-Analysis/Aspect based Senti analysis/aws/finalreviewscraper/')

    fileflipkart = name + '_flipkart'
    fileflipkart = re.sub(r'[^a-zA-Z0-9]', "_", fileflipkart)

    #check if the file already exists
    if os.path.exists("data/flipkart/"+fileflipkart+".json"):
        os.system("rm data/flipkart/"+fileflipkart+".json")

    os.system("scrapy crawl flipkartscraper -a ip='"+name+"' -o data/flipkart/"+fileflipkart+".json")

    fileamazon = name + '_amazon'
    fileamazon = re.sub(r'[^a-zA-Z0-9]', "_", fileamazon)

    #check if the file already exists
    if os.path.exists("data/amazon/"+fileamazon+".json"):
        os.system("rm data/amazon/"+fileamazon+".json")

    os.system("scrapy crawl amazonscraper -a ip='"+name+"' -o data/amazon/"+fileamazon+".json")

    get_aspects("data/amazon/"+fileamazon+".json","data/flipkart/"+fileflipkart+".json",name)

    #rendering data from files to the html output
    return render_template('review.html', AmazonReviews=json.load(open("/home/ubuntu/Aspect-Based-Sentiment-Analysis/Aspect based Senti analysis/aws/finalreviewscraper/data/amazon/"+fileamazon+".json")), FlipkartReviews=json.load(open("/home/ubuntu/Aspect-Based-Sentiment-Analysis/Aspect based Senti analysis/aws/finalreviewscraper/data/flipkart/"+fileflipkart+".json")))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
