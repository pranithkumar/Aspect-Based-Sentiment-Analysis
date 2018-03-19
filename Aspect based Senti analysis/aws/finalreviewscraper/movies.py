#This file runs a flask application that scrapes data from amazon and flipkart for specific products by executing scrapy spiders
from flask import Flask, render_template, redirect, url_for, request
import requests,json,os,sys,time,os.path,ast,string,re,numpy
from final_aspect_entity_extraction import *
from textblob import TextBlob

app = Flask(__name__, template_folder='.')

aspects_list = {}
aspects_top = []

#defining the homepage
@app.route('/')
def homepage():
    return render_template('movies.html')

@app.route('/chart')
def chart():
    return render_template('charts.html',labels=aspects_list.keys(), values=aspects_list.values(), aspects=aspects_top)

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

    aspects_dict = get_aspects("data/amazon/"+fileamazon+".json","data/flipkart/"+fileflipkart+".json",name)

    aspects_list = {}
    i=0
    for key, value in sorted(aspects_dict.iteritems(), key=lambda (k,v): (v,k),reverse = True):
        if i < 15:
            sent_score=[]
            for ke in aspects_dict[key].keys():
                wrd = key + ' ' + ke
                txt = TextBlob(wrd)
                sent_score.append(txt.sentiment.polarity)
            aspects_list[key.encode('utf-8')] = numpy.mean(sent_score)
            i=i+1

    FlipkartReviews=json.load(open("data/flipkart/"+fileflipkart+".json"))

    #rendering data from files to the html output
    #return render_template('dashboard.html', AmazonReviews=json.load(open("/home/ubuntu/Aspect-Based-Sentiment-Analysis/Aspect based Senti analysis/aws/finalreviewscraper/data/amazon/"+fileamazon+".json")), FlipkartReviews=json.load(open("/home/ubuntu/Aspect-Based-Sentiment-Analysis/Aspect based Senti analysis/aws/finalreviewscraper/data/flipkart/"+fileflipkart+".json")), labels=aspects_list.keys(), values=aspects_list.values())
    return render_template('dashboard.html', AmazonReviews=json.load(open("/home/ubuntu/Aspect-Based-Sentiment-Analysis/Aspect based Senti analysis/aws/finalreviewscraper/data/amazon/"+fileamazon+".json")), FlipkartReviews=json.dumps(FlipkartReviews), labels=aspects_list.keys(), values=aspects_list.values())

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
