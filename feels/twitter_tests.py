from TwitterAPI import *
from vaderSentiment.vaderSentiment import sentiment as vader
import re

#authentification
api = TwitterAPI('BQBZTbY3ugTypaRBq7Is0m6Dh', 'JGeRqs3r42Id4W2Q47NlGwAlNYv0myrBhlUPJeeizQXi56RWBm', auth_type='oAuth2')
print("authentification success\n")

name_query = "realdonaldtrump"
count = 10
r = api.request('statuses/user_timeline', {'screen_name': name_query, 'count':count, 'exclude_replies':'true', 'include_rts':'false'})

for item in r: #each tweet will be a Python dictionary
    
    # print item

    text = item['text'].encode('ascii', 'ignore')
    print text
    
    #clean_text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",text).split())
    # print clean_text


    print str(vs['compound'])