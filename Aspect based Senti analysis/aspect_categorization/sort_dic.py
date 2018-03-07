for k in sorted(mydict, key=lambda k: len(mydict[k]), reverse=True):
	print ' '.join(sorted(mydict[k], key=lambda ke: mydict[k][ke], reverse = True))
