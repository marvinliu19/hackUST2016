from TwitterAPI import *
from vaderSentiment.vaderSentiment import sentiment as vader
import re
import json

#authentification
api = TwitterAPI('BQBZTbY3ugTypaRBq7Is0m6Dh', 'JGeRqs3r42Id4W2Q47NlGwAlNYv0myrBhlUPJeeizQXi56RWBm', auth_type='oAuth2')
print("authentification success\n")

name_query = "realdonaldtrump" #THIS WILL BE NOT HARDCODED AND WILL BE TAKEN FROM THE FRONT END
count = 10
r = api.request('statuses/user_timeline', {'screen_name': name_query, 'count':count, 'exclude_replies':'true', 'include_rts':'false'})

personalInfoResponse = api.request('users/show', {'screen_name' : name_query, 'include_entities' : 'false'}).json()

realName = personalInfoResponse['name']
handle = personalInfoResponse['screen_name']
bio = personalInfoResponse['description']
profilePicture = personalInfoResponse['profile_image_url']
coverPhoto = personalInfoResponse['profile_banner_url']

pyDictionary = {'name' : realName, 'handle' : handle, 'bio' : bio, 'profilePicture' : profilePicture, 'coverPhoto' : coverPhoto, "tweets" : []}


for item in r: #each tweet will be a Python dictionary
    
    text = item['text'].encode('ascii', 'ignore')
    date = item['created_at'].encode('ascii', 'ignore')
    retweet_count = item['retweet_count']
    feels = vader(text)

    tempDict = {"text" : text, "date" : date, "retweet_count" : retweet_count, "feels" : feels}
    pyDictionary["tweets"].append(tempDict)
    
jsonObjectToPassToFront = json.dumps(pyDictionary) #this object is the output
print "Success!"