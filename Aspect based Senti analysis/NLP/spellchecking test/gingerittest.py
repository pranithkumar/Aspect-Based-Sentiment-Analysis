from gingerit.gingerit import GingerIt

text = '''best phone for photography lovers in this price tag..GO FOR IT.. BUT BEFORE THAT YOU SHOULD KNOW YOUR PRIORITY.. 
 
DISPLAY QUALITY  ALSO GOOD(FHD) 
BATTERY  BACKUP AWESOME (AVG 8HOURS SOT)
UI ALSO HIGHLY CUSTOMISED.. 
PHONE LOOKS GREAT WITH DUAL CAMERA

CONS-audio output through  speaker  is not so loud.. same case in case of earphone(it's sound quality  good but not so loud)

2nd sim slot only supports only 2g..

HIGH QUALITY  GAME, (bigger than 2gb) lag sometimes.. 

ACCORDING  TO MY OPINION This phone is great.... go for it.. rest depends  on your choice. THANKS.'''

parser = GingerIt()
result = parser.parse(text)

print "text: "+result['text']+"\nresult: "+result['result']