from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

choices = ['', 'con i', 'battery untill', 'looks', 'touch', 'speed', 'dont', 'update i', 'situations', 'window', 'winner', 'ram management', 'feel', 'charge', 'usage', 'camera quality', 'damages', 'case', 'advantage', 'views', 'game', 'bilion day', 'fingerprint', 'front', 'bit', 'day', 'color', 'disply', 'similer', 'signal reception', 'quality game', 'quality mobile', 'signal', 'honor', 'emui', 'mode', 'output', 'flipkart', 'mode picture', 'deal', 'people', 'branding', 'noise', 'design', 'honor mobile', 'build quality', 'review', 'power savng', 'aperture mode', 'everything', 'finger', 'sensor', 'satisfy', 'camera clarity', 'power', 'use granuels', 'confusion', 'screen', 'use', 'update', 'efficiency', 'packing', 'sensors', 'bilion', 'front camera', 'heating', 'amount', 'backup', 'processor', 'software', 'load', 'features', 'criterias', 'battery', 'image', 'batry', 'dont use', 'everyone', 'delevery', 'shoots', 'quality', 'story', 'management', 'service', 'usage i', 'look cons', 'battery backup', 'camera', 'criteria', 'aperture', 'legs', 'batrry', 'mobiles', 'function', 'cricket', 'buy', 'delivery', 'phone', 'part', 'sound', 'look', 'camera cons', 'advantage charging', 'n', 'mobile', 'ui', 'today', 'problem', 'piece', 'display', 'compare', 'earphone', 'ram', 'life', 'doesn', 'camera awesome', 'guarantee', 'sound quality', 'make', 'get', 'nd', 'feature', 'note', 'amazing', 'speaker', 'build', 'speed network', 'android', 'charging', 'sim', 'okay', 'beauty', 'though', 'price', 'effect', 'jst', 'thankyou', 'device', 'mah', 'data', 'response', 'purchase', 'calls', 'i', 'light', 'nd sel', 'options', 'phone value', 'con', 'reception', 'time', 'rupees', 'notch']

i=0
for choice in choices[:-1]:
	for check in choices[i+1:]:
		if similar(choice,check)>0.55:
			print "comparing similarity of "+choice+" and "+check
			print similar(choice,check)
	i += 1