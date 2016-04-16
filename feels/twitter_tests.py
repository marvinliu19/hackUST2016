from TwitterAPI import *
from vaderSentiment.vaderSentiment import sentiment as vader

#authentification
api = TwitterAPI('BQBZTbY3ugTypaRBq7Is0m6Dh', 'JGeRqs3r42Id4W2Q47NlGwAlNYv0myrBhlUPJeeizQXi56RWBm', auth_type='oAuth2')
print("authentification success\n")

myQuery = "Donald Trump"
count = 10
r = api.request('search/tweets', {'q': myQuery, 'lang': 'en', 'count':count})

for item in r: #each tweet will be a Python dictionary
    text = item['text'].encode('ascii', 'ignore')
    print text
    vs = vader(text)
    print("\n\t" + str(vs))