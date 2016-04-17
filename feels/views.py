import json
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from TwitterAPI import *
from vaderSentiment.vaderSentiment import sentiment as vader
import re
from collections import Counter as count

from .forms import QueryForm

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

def build_bio_dict(personalInfo):
    "builds bio dictionary with raw tweeter user's info"
    realName = personalInfo['name']
    handle = personalInfo['screen_name']
    followers = personalInfo['followers_count']
    # We need to check the existence of the following fields
    # if they don't exist we create empty one
    if 'description' in personalInfo:
        bio = personalInfo['description']
    else:
        bio = ""
    if 'profile_image_url' in personalInfo:
        profilePicture = personalInfo['profile_image_url']
    else:
        profilePicture = ""
    if 'profile_banner_url' in personalInfo:
        coverPhoto = personalInfo['profile_banner_url']
    else:
        coverPhoto = ""

    bio_dict = {'name' : realName, 'handle' : handle, 'bio' : bio, 'profilePicture' : profilePicture, 'coverPhoto' : coverPhoto, 'followers' : followers}
    return bio_dict

def build_tweets_dict(tweets):
    "builds tweets dictionary with raw tweeter tweets"
    tweets_dict = {'tweets': []}
    for tweet in tweets: #each tweet will be a Python dictionary
        text = tweet['text'].encode('ascii', 'ignore')
        text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",text).split())
        text.strip()

        if text == "":
            continue

        date = tweet['created_at'].encode('ascii', 'ignore')
        retweet_count = tweet['retweet_count']
        sentiment = vader(text)

        tweet_data = {"text" : text, "date" : date, "retweet_count" : retweet_count, "sentiment" : sentiment}
        tweets_dict["tweets"].insert(0, tweet_data)

    return tweets_dict

def extract_hashtags(s):
    return [i for i in s.split() if i.startswith("#") ]

def build_hashtag_freq(tweets):
    hashtag_counts = {}
    for tweet in tweets: #each tweet will be a Python dictionary
        hashtags = extract_hashtags(tweet['text'].encode('ascii', 'ignore'))
        for hashtag in hashtags:
            if hashtag in hashtag_counts:
                hashtag_counts[hashtag] += 1
            else:
                hashtag_counts[hashtag] = 1

    top_hashtags = {'hashtags': []}

    hashtag_counts = count(hashtag_counts)
    for k, v in hashtag_counts.most_common(7):
        top_hashtags['hashtags'].append([k, v])
    return top_hashtags

def build_other_tweets(tweets):
    tweets_dict = {'tweets': [], 'sentiment_count': {'Positive': 0, 'Neutral': 0, 'Negative':0}}
    
    for tweet in tweets: #each tweet will be a Python dictionary
        text = tweet['text'].encode('ascii', 'ignore')
        text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",text).split())
        text.strip()

        if text == "":
            continue

        date = tweet['created_at'].encode('ascii', 'ignore')
        retweet_count = tweet['retweet_count']
        sentiment = vader(text)

        if sentiment['compound'] < -0.1:
            tweets_dict['sentiment_count']['Negative'] += 1
        elif sentiment['compound'] > 0.1:
            tweets_dict['sentiment_count']['Positive'] += 1
        else:
            tweets_dict['sentiment_count']['Neutral'] += 1

        tweet_data = {"text" : text, "date" : date, "retweet_count" : retweet_count, "sentiment" : sentiment}
        tweets_dict["tweets"].insert(0, tweet_data)

    return tweets_dict


def index(request):
    form = QueryForm()
    context = RequestContext(request, {'form': form})
    return render_to_response('feels/index.html', context)

def display(request):
    context = {}
    bio_output = ""
    tweets_output = ""

    name_query = 'kanyewest'

    if request.method == "POST":
        name_query = request.POST['query_text']
        name_query = name_query.replace('@', '')
    


  # Authentification
    api = TwitterAPI('BQBZTbY3ugTypaRBq7Is0m6Dh', 'JGeRqs3r42Id4W2Q47NlGwAlNYv0myrBhlUPJeeizQXi56RWBm', auth_type='oAuth2')



    # requests to twitter, one for one's tweet the other for one's personal info
    count = 200
    tweets = api.request('statuses/user_timeline', {'screen_name': name_query, 'count':count, 'exclude_replies':'true', 'include_rts':'false'})
    otherTweets = api.request('search/tweets', {'q': '@'+name_query, 'count':count, 'lang': 'en'});
    personalInfoResponse = api.request('users/show', {'screen_name' : name_query, 'include_entities' : 'false'}).json()

    # Error testing, if user not found, we search for one
    if 'errors' in personalInfoResponse:
        error = personalInfoResponse['errors']
        name_query = 'kanyewest'
        tweets = api.request('statuses/user_timeline', {'screen_name': name_query, 'count':count, 'exclude_replies':'true', 'include_rts':'false'})
        personalInfoResponse = api.request('users/show', {'screen_name' : name_query, 'include_entities' : 'false'}).json()
        bio_output = json.dumps(build_bio_dict(personalInfoResponse))
        tweets_output = json.dumps(build_tweets_dict(tweets))
        top_hashtags = json.dumps(build_hashtag_freq(tweets))
        context = {
            'query': name_query
        }

        context = RequestContext(request, context)
        context['bio_data'] = bio_output
        context['tweet_data'] = tweets_output
        context['top_hashtags'] = top_hashtags

        return render_to_response('feels/display.html', context)

    else:
        bio_output = json.dumps(build_bio_dict(personalInfoResponse))
        tweets_output = json.dumps(build_tweets_dict(tweets))
        top_hashtags = json.dumps(build_hashtag_freq(tweets))
        other_tweets_output = json.dumps(build_other_tweets(otherTweets))
        context = {
          'query': name_query
        }

        context = RequestContext(request, context)
        context['bio_data'] = bio_output
        context['tweet_data'] = tweets_output
        context['top_hashtags'] = top_hashtags
        context['other_tweets'] = other_tweets_output

        return render_to_response('feels/display.html', context)