from TwitterAPI import *
from vaderSentiment.vaderSentiment import sentiment as vader
import re
import json

def search_users(query):
    "performs a user/search query and returns list of most relevant users name"
    # needs a connection with oAuth1 ie with user credentials
    # we use Jafeel2 ;)
    consumer_key = 'ZuFJRql4R1wLe3vOP9IcD8B5t'
    consumer_secret = 'XtrinZVQbvHYCcc0IpHDG7NA4DuocdjHIdQ1Dt7u5w8vkxhonk'
    access_token_key = '137058679-CVBZBXfDCyox60tWZVbHcHK1cSWROXzxjzRfdO6s'
    access_token_secret = 'yS2Zb2g5pD4QuUbgYRFt966xPqfmB3AZzlbfeKd0Nrbyo'
    api2 = TwitterAPI(consumer_key,
                 consumer_secret,
                 access_token_key,
                 access_token_secret)
    page = 1
    nb_results = 10
    # r = api2.request('users/search', {'q':query, 'count':nb_results }).json()
    r = api2.request('users/search', {'q':query, 'page':page, 'count':nb_results }).json()
    
    user_list = []
    for item in r:
        user_list.append(item['screen_name'])

    print user_list
    return user_list


#authentification
api = TwitterAPI('BQBZTbY3ugTypaRBq7Is0m6Dh', 'JGeRqs3r42Id4W2Q47NlGwAlNYv0myrBhlUPJeeizQXi56RWBm', auth_type='oAuth2')
print("authentification success\n")

name_query = "trump" #THIS WILL BE NOT HARDCODED AND WILL BE TAKEN FROM THE FRONT END
count = 10

# requests to twitter, one for one's tweet the other for one's personal info
r = api.request('statuses/user_timeline', {'screen_name': name_query, 'count':count, 'exclude_replies':'true', 'include_rts':'false'})
personalInfoResponse = api.request('users/show', {'screen_name' : name_query, 'include_entities' : 'false'}).json()

if 'errors' in personalInfoResponse:
    error = personalInfoResponse['errors']
    print error[0]['message']
    if error[0]['code'] == 50:
        #user not found
        search_users(name_query)



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