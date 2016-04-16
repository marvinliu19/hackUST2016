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
    if request.method == "POST":
      api = TwitterAPI('BQBZTbY3ugTypaRBq7Is0m6Dh', 'JGeRqs3r42Id4W2Q47NlGwAlNYv0myrBhlUPJeeizQXi56RWBm', auth_type='oAuth2')
      myQuery = request.POST['query']  # takes in query from front-end
      r = api.request('search/tweets', {'q': myQuery})
      context = {  # adds query and JSON response of tweets to context
          'query': myQuery,
          'response': r
      }
      context = RequestContext(request, context)
    return render_to_response('feels/display.html', context)