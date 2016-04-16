from django import *
from TwitterAPI import *

def index(request):
    context = {}
    #post request means we parse for a query
    if request.method == 'POST':
        api = TwitterAPI('BQBZTbY3ugTypaRBq7Is0m6Dh', 'JGeRqs3r42Id4W2Q47NlGwAlNYv0myrBhlUPJeeizQXi56RWBm', auth_type='oAuth2')
        myQuery = request.POST['query'] #takes in query from front-end
        r = api.request('search/tweets', {'q': myQuery})
        '''
        for item in r:
            print(item)
        '''
        context = {  # adds query and JSON response of tweets to context
            'query': myQuery,
            'response': r
        }

    return render(request, 'feels/index.html', context)

def display(request):
  context = {}
  return render(request, 'feels/display.html', context)