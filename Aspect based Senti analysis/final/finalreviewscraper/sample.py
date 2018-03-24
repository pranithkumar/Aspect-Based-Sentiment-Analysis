from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import random

def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 83%, 50%)"

aspects_wc = {'money': (0.436, -0.027), 'colors': (0.4, -0.056), 'gb': (0.286, 0.0), 'go': (0.633, 0.0), 'issues': (0.35, 0.0), 'lg': (0.3, -0.125), 'blast': (0.2, 0.0), 'thank': (0.557, 0.0), 'lukng': (0.7, 0.0), 'platform': (0.6, 0.0), 'charge': (0.188, -0.025), 'offers': (0.129, 0.0), 'whatsapp': (0.0, -0.275), 'oct': (0.6, 0.0), 'amazon': (0.563, -0.017), 'hands': (0.2, 0.0), 'sony': (0.645, 0.0), 'bit': (0.05, -0.094), 'phn lookwise': (0.263, -0.047), 'qualityy': (0.7, 0.0), 'shots': (0.133, -0.275), 'hype': (0.6, 0.0), 'thanks': (0.261, 0.0), 'deal': (0.6, -0.167), 'people': (0.0, 0.0), 'touch': (0.067, -0.183), 'cost': (0.0, 0.0), 'displays': (0.5, 0.0), 'reasons': (0.4, 0.0), 'description': (0.418, 0.0), 'delivery date': (0.286, 0.0), 'seller': (0.458, 0.0), 'lag cons': (0.6, 0.0), 'issue': (0.4, 0.0), 'ios': (0.358, -0.083), 'z5': (0.645, 0.0), 'card': (0.0, 0.0), 'batery': (0.263, -0.047), 'box': (0.0, 0.0), 'brilliant': (0.808, 0.0), 'heating': (0.367, 0.0), 'experience': (0.543, -0.143), 'thing': (0.0, -0.275), 'products': (0.2, -0.35), 'name nothing': (0.6, 0.0), 'dis': (0.367, 0.0), 'scare': (0.2, 0.0), 'features': (0.75, 0.0), 'diwali sale': (0.0, 0.0), 'battery': (0.425, -0.05), 'packaging': (0.303, -0.025), 'quality': (0.53, -0.031), 'gona blast': (0.2, 0.0), 'service': (0.7, 0.0), 'apps': (0.0, -0.386), 'camera': (0.414, -0.085), 'cashback': (0.0, 0.0), 'way': (0.6, 0.0), 'call': (0.233, -0.167), 'flipkart': (0.229, -0.212), 'buy': (0.526, 0.0), 'shopping': (0.265, -0.031), 'brand': (0.35, -0.25), 'delivery': (0.233, -0.248), 'averge': (0.3, -0.125), 'october': (0.36, 0.0), 'look': (0.233, -0.3), 'hour': (0.0, 0.0), 'value': (0.364, -0.098), 'n': (0.367, 0.0), 'reviews': (0.119, -0.163), 'problem': (0.434, -0.007), 'piece': (0.7, 0.0), 'f2': (0.133, -0.275), 'cons': (0.267, -0.167), 'gona': (0.2, 0.0), 'lock': (0.645, 0.0), 'worry': (0.05, -0.094), 'till': (0.6, 0.0), 'authentication': (0.0, -0.188), 'camera quality': (0.225, -0.075), 'online': (0.125, -0.094), 'performance': (0.65, 0.0), 'android': (0.175, -0.272), 'product': (0.433, -0.087), 'phn': (0.482, -0.042), 'price': (0.404, -0.053), 'lag': (0.6, 0.0), 'problems': (0.1, -0.125), 'belive': (0.2, 0.0), 'device': (0.467, -0.1), 'customer care': (0.5, 0.0), 'purchase': (0.31, -0.037), 'drain': (0.263, -0.047), 'thz': (0.7, 0.0), 'mobile': (0.539, 0.0), 'charger': (0.3, 0.0), 'sale': (0.463, -0.063), 'delivery product': (0.418, 0.0), 'order': (0.179, -0.094)}

positive = {}
negative = {}

for i in aspects_wc:
	if aspects_wc[i][0]!=0.0:
		positive[i] = aspects_wc[i][0]
	if aspects_wc[i][1]!=0.0:
		negative[i] = aspects_wc[i][1]


positive_img = np.array(Image.open("thumbup.png"))
negative_img = np.array(Image.open("thumbdown.png"))

#wordcloud_pos = WordCloud(background_color=None, mode="RGBA",mask=positive_img ,width=500,height=500, max_words=1628,relative_scaling=1,normalize_plurals=False).generate_from_frequencies(positive)

wordcloud_neg = WordCloud(background_color=None, mode="RGBA",mask=negative_img ,width=500,height=500, max_words=1628,relative_scaling=1,normalize_plurals=False).generate_from_frequencies(negative)

#image_colors = ImageColorGenerator(negative_img)

#plt.imshow(wordcloud_pos.recolor(color_func=grey_color_func, random_state=3), interpolation="bilinear")

#plt.axis("off")
#plt.savefig("wordcloud_pos.png",transparent=True)
#plt.show()

#plt.close()
plt.imshow(wordcloud_neg.recolor(color_func=grey_color_func, random_state=3), interpolation="bilinear")

plt.axis("off")
plt.savefig("wordcloud_neg.png",transparent=True)
plt.show()