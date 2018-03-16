#This file runs a flask application that scrapes data from amazon and flipkart for specific products by executing scrapy spiders
from flask import Flask, render_template, redirect, url_for, request
import requests,json,os,sys,time,os.path,ast,string,re,numpy
from final_aspect_entity_extraction import *
from textblob import TextBlob

app = Flask(__name__, template_folder='.')

#defining the homepage
@app.route('/')
def homepage():
    return render_template('index.html')

#taking the search keyword as input
@app.route('/test',methods = ['POST', 'GET'])
def login():
    user = request.args.get('nm')
    return redirect(url_for('success',name = user))

#function that executes the spiders and stores the output in json files
@app.route('/success/<name>')
def success(name):
    #storing input search keyword in input.txt
    f = open('input.txt','w')
    f.write(name)
    f.close()

    os.system("scrapy crawl searchspiderflipkart")

    #extracting filename of the json file to be stored from productlinkflipkart.txt
    '''f = open('productlinkflipkart.txt','r')
    filenameflipkart = f.read()
    f.close()
    fileflipkart=filenameflipkart.split('/')[1]'''
    fileflipkart = name + '_flipkart'
    fileflipkart = re.sub(r'[^a-zA-Z0-9]', "_", fileflipkart)

    #check if the file already exists
    if os.path.exists("data/flipkart/"+fileflipkart+".json"):
        os.system("rm data/flipkart/"+fileflipkart+".json")

    os.system("scrapy crawl completeflipkartscraper -o data/flipkart/"+fileflipkart+".json")

    os.system("scrapy crawl searchspideramazon")

    os.system("scrapy crawl getproductspideramazon")

    #extracting filename of the json file to be stored from productlinkamazon.txt
    '''f = open('productlinkamazon.txt','r')
    filenameamazon = f.read()
    f.close()
    fileamazon=filenameamazon.split('/')[1]'''
    fileamazon = name + '_amazon'
    fileamazon = re.sub(r'[^a-zA-Z0-9]', "_", fileamazon)

    #check if the file already exists
    if os.path.exists("data/amazon/"+fileamazon+".json"):
        os.system("rm data/amazon/"+fileamazon+".json")

    os.system("scrapy crawl completeamazonscraper -o data/amazon/"+fileamazon+".json")

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

    #rendering data from files to the html output
    return render_template('dashboard.html', AmazonReviews=json.load(open("data/amazon/"+fileamazon+".json")), FlipkartReviews=json.load(open("data/flipkart/"+fileflipkart+".json")), labels=aspects_list.keys(), values=aspects_list.values())

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
