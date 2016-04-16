from django.http import HttpResponseRedirect
from django.shortcuts import render

def index(request):
    context = {}
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        myQuery = request.POST['query'] #takes in query from front-end
        context = { #adds query to context
            'query': myQuery
        }
    return render(request, 'feels/index.html', context)

def display(request):
  context = {}
  return render(request, 'feels/display.html', context)