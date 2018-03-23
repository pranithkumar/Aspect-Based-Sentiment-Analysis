#This file runs a flask application that scrapes data from amazon and flipkart for specific products by executing scrapy spiders
from flask import Flask, render_template, redirect, url_for, request
import requests,json,os,sys,time,os.path,ast,string,re,numpy,random
from final_aspect_entity_extraction import *
from textblob import TextBlob
from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image

app = Flask(__name__, template_folder='.',static_url_path='/static')

aspects_list = {}
aspects_wc = {}
aspects_top = []
wordcloud_count = 0

def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(0, 1)

#defining the homepage
@app.route('/')
def homepage():
    return render_template('index.html')

#taking the search keyword as input
@app.route('/test',methods = ['POST', 'GET'])
def login():
    user = request.args.get('nm')
    return redirect(url_for('success',name = user))

@app.route('/chart')
def chart():
    global wordcloud_count
    positive = {}
    negative = {}

    for i in aspects_wc:
        if aspects_wc[i][0]!=0.0:
            positive[i] = aspects_wc[i][0]
        if aspects_wc[i][1]!=0.0:
            negative[i] = aspects_wc[i][1]


    positive_img = numpy.array(Image.open("thumbup.png"))
    negative_img = numpy.array(Image.open("thumbdown.png"))

    wordcloud_pos = WordCloud(background_color=None, mode="RGBA",mask=positive_img ,width=900,height=500, max_words=1628,relative_scaling=1,normalize_plurals=False).generate_from_frequencies(positive)

    wordcloud_neg = WordCloud(background_color=None, mode="RGBA",mask=negative_img ,width=900,height=500, max_words=1628,relative_scaling=1,normalize_plurals=False).generate_from_frequencies(negative)

    #image_colors = ImageColorGenerator(negative_img)
    plt.close()
    plt.imshow(wordcloud_pos.recolor(color_func=grey_color_func, random_state=3), interpolation="bilinear")

    plt.axis("off")
    plt.savefig("static/wordcloud_pos.png",transparent=True)
    #plt.show()
    plt.close()

    plt.imshow(wordcloud_neg.recolor(color_func=grey_color_func, random_state=3), interpolation="bilinear")

    plt.axis("off")
    plt.savefig("static/wordcloud_neg.png",transparent=True)
    wordcloud_count+=1
    #plt.show()
    return render_template('charts.html',labels=aspects_list.keys(), values=aspects_list.values(), aspects=aspects_top,count=wordcloud_count)

#function that executes the spiders and stores the output in json files
@app.route('/success/<name>')
def success(name):

    now = time.time()
    old = now - 7 * 24 * 60 * 60
    global aspects_top
    global aspects_list
    global aspects_wc

    if os.path.exists("static/wordcloud_pos.png"):
        os.remove("static/wordcloud_pos.png")
    if os.path.exists("static/wordcloud_neg.png"):
        os.remove("static/wordcloud_neg.png")

    fileflipkart = name + '_flipkart'
    fileflipkart = re.sub(r'[^a-zA-Z0-9]', "_", fileflipkart)

    #check if the file already exists
    if os.path.exists("data/flipkart/"+fileflipkart+".json"):
        stat = os.stat("data/flipkart/"+fileflipkart+".json")
        if stat.st_ctime < old:
            print "removing: data/flipkart/"+fileflipkart+".json"
            os.remove("data/flipkart/"+fileflipkart+".json")
            os.system("scrapy crawl flipkartscraper -a ip='"+name+"' -o data/flipkart/"+fileflipkart+".json")
    else:
        os.system("scrapy crawl flipkartscraper -a ip='"+name+"' -o data/flipkart/"+fileflipkart+".json")

    fileamazon = name + '_amazon'
    fileamazon = re.sub(r'[^a-zA-Z0-9]', "_", fileamazon)

    #check if the file already exists
    if os.path.exists("data/amazon/"+fileamazon+".json"):
        stat = os.stat("data/amazon/"+fileamazon+".json")
        if stat.st_ctime < old:
            print "removing: data/flipkart/"+fileamazon+".json"
            os.remove("data/flipkart/"+fileamazon+".json")
            os.system("scrapy crawl amazonscraper -a ip='"+name+"' -o data/amazon/"+fileamazon+".json")
    else:
        os.system("scrapy crawl amazonscraper -a ip='"+name+"' -o data/amazon/"+fileamazon+".json")

    aspects_dict = get_aspects("data/amazon/"+fileamazon+".json","data/flipkart/"+fileflipkart+".json",name)

    del aspects_top[:]
    aspects_list.clear()
    aspects_wc.clear()

    i=0
    for key, value in sorted(aspects_dict.iteritems(), key=lambda (k,v): (v,k),reverse = True):
        if i < 100:
            navg=0.0
            pavg=0.0
            if i<10:
                aspects_top.append((key.encode('utf-8'),len(value)))
            sent_score_pos=[]
            sent_score_neg=[]
            for ke in aspects_dict[key].keys():
                wrd = key + ' ' + ke
                txt = TextBlob(wrd)
                score = txt.sentiment.polarity
                if score>0:
                    sent_score_pos.append(score)
                elif score<0:
                    sent_score_neg.append(score)
            if sent_score_pos:
                pavg = numpy.sum(sent_score_pos)/(len(sent_score_pos)+len(sent_score_neg))
            if sent_score_neg:
                navg = numpy.sum(sent_score_neg)/(len(sent_score_pos)+len(sent_score_neg))
            if i<10:
                aspects_list[key.encode('utf-8')] = (round(pavg,3),round(navg,3))
            aspects_wc[key.encode('utf-8')] = (round(pavg,3),round(navg,3))
            i=i+1


    #rendering data from files to the html output
    if os.stat("data/amazon/"+fileamazon+".json").st_size == 0:
        return render_template('dashboard.html', AmazonReviews=[], FlipkartReviews=json.load(open("data/flipkart/"+fileflipkart+".json")), labels=aspects_list.keys(), values=aspects_list.values(), aspects=aspects_top)
    elif os.stat("data/flipkart/"+fileflipkart+".json").st_size == 0:
        return render_template('dashboard.html', AmazonReviews=json.load(open("data/amazon/"+fileamazon+".json")), FlipkartReviews=[], labels=aspects_list.keys(), values=aspects_list.values(), aspects=aspects_top)
    else:
        return render_template('dashboard.html', AmazonReviews=json.load(open("data/amazon/"+fileamazon+".json")), FlipkartReviews=json.load(open("data/flipkart/"+fileflipkart+".json")), labels=aspects_list.keys(), values=aspects_list.values(), aspects=aspects_top)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
