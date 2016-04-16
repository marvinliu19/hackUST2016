from TwitterAPI import *
import json


#authentification
api = TwitterAPI('BQBZTbY3ugTypaRBq7Is0m6Dh', 'JGeRqs3r42Id4W2Q47NlGwAlNYv0myrBhlUPJeeizQXi56RWBm', auth_type='oAuth2')
print("authentification success\n")

myQuery = "Donald Trump"
r = api.request('search/tweets', {'q': myQuery, 'lang': 'en'})

for item in r: #each tweet will be a Python dictionary
    print(item['text'].encode('ascii', 'ignore'))