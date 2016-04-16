import json
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from TwitterAPI import *
from vaderSentiment.vaderSentiment import sentiment as vader
import re

from .forms import QueryForm

def index(request):
  form = QueryForm()
  context = RequestContext(request, {'form': form})
  return render_to_response('feels/index.html', context)

def display(request):
  context = {}
  bio_output = ""
  tweets_output = ""

  if request.method == "POST":
    api = TwitterAPI('BQBZTbY3ugTypaRBq7Is0m6Dh', 'JGeRqs3r42Id4W2Q47NlGwAlNYv0myrBhlUPJeeizQXi56RWBm', auth_type='oAuth2')
    name_query = request.POST['query_text']
    count = 10
    tweets = api.request('statuses/user_timeline', {'screen_name': name_query, 'count':count, 'exclude_replies':'true', 'include_rts':'false'})

    personalInfoResponse = api.request('users/show', {'screen_name' : name_query, 'include_entities' : 'false'}).json()

    realName = personalInfoResponse['name']
    handle = personalInfoResponse['screen_name']
    bio = personalInfoResponse['description']
    profilePicture = personalInfoResponse['profile_image_url']
    coverPhoto = personalInfoResponse['profile_banner_url']

    bio_dict = {'name' : realName, 'handle' : handle, 'bio' : bio, 'profilePicture' : profilePicture, 'coverPhoto' : coverPhoto}
    tweets_dict = {'tweets': []}
    for tweet in tweets: #each tweet will be a Python dictionary
      text = tweet['text'].encode('ascii', 'ignore')
      text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",text).split())
      
      date = tweet['created_at'].encode('ascii', 'ignore')
      retweet_count = tweet['retweet_count']
      sentiment = vader(text)

      tweet_data = {"text" : text, "date" : date, "retweet_count" : retweet_count, "sentiment" : sentiment}
      tweets_dict["tweets"].insert(0, tweet_data)
    
    bio_output = json.dumps(bio_dict)
    tweets_output = json.dumps(tweets_dict)

    context = {
      'query': name_query
    }

  context = RequestContext(request, context)
  context['bio_data'] = bio_output
  context['tweet_data'] = tweets_output

  context['feeling_data'] = json.dumps({'January': -0.2, 'February': -0.5, 'March': 0.1, 'April':0.3, 'May': 0.2, 'June': 0.6, 'July': 0.3})
  context['retweet_data'] = json.dumps({'January': 2341, 'February': 1232, 'March': 9083, 'April':2032, 'May': 1032, 'June': 821, 'July': 1454})

  return render_to_response('feels/display.html', context)