#This file runs a flask application that scrapes data from amazon and flipkart for specific products by executing scrapy spiders
from flask import Flask, render_template, redirect, url_for, request
import requests,json,os,sys,time,os.path,ast,string

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
    f = open('input.txt','w')
    f.write(name)
    f.close()

    os.chdir('/home/pranith/project/Aspect-Based-Sentiment-Analysis/Aspect based Senti analysis/data_scraping/reviewscraper/')

    os.system("scrapy crawl searchspiderflipkart")

    #extracting filename of the json file to be stored from productlinkflipkart.txt
    '''f = open('productlinkflipkart.txt','r')
    filenameflipkart = f.read()
    f.close()
    fileflipkart=filenameflipkart.split('/')[1]'''
    fileflipkart = name + '_flipkart'
    fileflipkart = string.replace(fileflipkart,' ','_')

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
    fileamazon = string.replace(fileamazon,' ','_')

    #check if the file already exists
    if os.path.exists("data/amazon/"+fileamazon+".json"):
        os.system("rm data/amazon/"+fileamazon+".json")

    os.system("scrapy crawl completeamazonscraper -o data/amazon/"+fileamazon+".json")

    #rendering data from files to the html output
    return render_template('review.html', AmazonReviews=json.load(open("data/amazon/"+fileamazon+".json")), FlipkartReviews=json.load(open("data/flipkart/"+fileflipkart+".json")))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
