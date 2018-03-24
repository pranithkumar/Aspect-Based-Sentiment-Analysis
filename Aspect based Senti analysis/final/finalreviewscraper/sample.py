import json,pandas,os
if os.stat("data/flipkart/yonix_carbonex_flipkart.json").st_size==0:
	print "true"
else:
	print "false"
