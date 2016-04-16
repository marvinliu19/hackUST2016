import json
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from TwitterAPI import *

from .forms import QueryForm

def index(request):
  form = QueryForm()
  context = RequestContext(request, {'form': form})
  return render_to_response('feels/index.html', context)

def display(request):
    context = {}

    if request.method == "POST":
        api = TwitterAPI('BQBZTbY3ugTypaRBq7Is0m6Dh', 'JGeRqs3r42Id4W2Q47NlGwAlNYv0myrBhlUPJeeizQXi56RWBm', auth_type='oAuth2')
        myQuery = request.POST['query_text']  # takes in query from front-end
        r = api.request('search/tweets', {'q': myQuery})
        
        context = {
            'query': myQuery,
        }

    context = RequestContext(request, context)
    context['feeling_data'] = json.dumps({'January': -0.2, 'February': -0.5, 'March': 0.1, 'April':0.3, 'May': 0.2, 'June': 0.6, 'July': 0.3})
    context['retweet_data'] = json.dumps({'January': 2341, 'February': 1232, 'March': 9083, 'April':2032, 'May': 1032, 'June': 821, 'July': 1454})

    return render_to_response('feels/display.html', context)

