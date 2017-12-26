import requests
from bs4 import BeautifulSoup

def scrape_flipkart(url, no_products):
	r = requests.get(url)

	soup = BeautifulSoup(r.content,"lxml")
	#print soup

	data = soup.find_all("div", {"class":"_3liAhj"})
	#print data
	product_name = []
	image_url = []
	price = []
	link = []
	for item in data:
	    name = item.find_all("a",{"class":"_2cLu-l"})[0]
	    product_name.append(name.get("title"))
	    image = item.find_all("img")[0]
	    #print image
	    if image.get("data-src"):
	    	img_url = image.get("data-src")
	    else:
	    	img_url = image.get("src")
	    	#print img_url
	    	image_url.append(img_url)
	    	price1 = item.find_all("div",{"class":"_1vC4OE"})[0]
	    	price.append(price1.text.strip())
	    	link.append(name.get("href"))
	product_name_final = product_name[:no_products]
	image_url_final = image_url[:no_products]
	price_final = price[:no_products]
	link_final = link[:no_products]
	print "product names:"
	print product_name_final
	print "image urls"
	print image_url_final
	print "prices"
	print price_final
	print "links"
	print link_final

if __name__ == '__main__':
	print "Starting Product population script..."
 
print '\n\n----------------------Flipkart Scraping Script------------------------\n\n'

print '\nMens Watches\n'

scrape_flipkart('http://www.flipkart.com/watches/pr?p%5B%5D=facets.ideal_for%255B%255D%3DMen&p%5B%5D=sort%3Dpopularity&sid=r18&facetOrder%5B%5D=ideal_for&otracker=ch_vn_watches_men_nav_catergorylinks_0_AllBrands', 5)
