from gingerit.gingerit import GingerIt

text = 'The phne is the bst in low cst mobiles and its features are grt.'

parser = GingerIt()
result = parser.parse(text)

print "text: "+result['text']+"\nresult: "+result['result']