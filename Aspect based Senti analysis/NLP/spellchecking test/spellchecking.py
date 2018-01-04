from autocorrect import spell
text = "this is good gloroius speling books phnoe"
tokens = text.split(' ')
result = ''
for s in tokens:
    result += spell(s)+" "
print result