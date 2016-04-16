from TwitterAPI import *
from vaderSentiment.vaderSentiment import sentiment as vader
import re

#authentification
api = TwitterAPI('BQBZTbY3ugTypaRBq7Is0m6Dh', 'JGeRqs3r42Id4W2Q47NlGwAlNYv0myrBhlUPJeeizQXi56RWBm', auth_type='oAuth2')
print("authentification success\n")

myQuery = "Donald Trump"
count = 10
tweets = api.request('search/tweets', {'q': myQuery, 'lang': 'en', 'geocode': '37.781157,-122.398720, 6371km','count':count})

for tweet in tweets:
    text = tweet['text'].encode('ascii', 'ignore')
    clean_text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",text).split())
    print clean_text
    print tweet['geo']
    vs = vader(clean_text)

    print str(vs['compound'])