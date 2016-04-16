from TwitterAPI import *
from vaderSentiment import vaderSentiment


#authentification
api = TwitterAPI('BQBZTbY3ugTypaRBq7Is0m6Dh', 'JGeRqs3r42Id4W2Q47NlGwAlNYv0myrBhlUPJeeizQXi56RWBm', auth_type='oAuth2')
print("authentification success\n")

myQuery = "Donald Trump"
count = 10
r = api.request('search/tweets', {'q': myQuery, 'lang': 'en', 'count':count})

for item in r: #each tweet will be a Python dictionary
    print(item['text'].encode('ascii', 'ignore'))
    vs = vaderSentiment.sentiment("hey w4tasrtgawg")
    print("\n\t" + str(vs))