from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from .forms import QueryForm

def index(request):
  form = QueryForm()
  context = RequestContext(request, {'form': form})
  return render_to_response('feels/index.html', context)

def display(request):
  if request.method == "POST":
    query = request.POST['query_text']
    context = {
               'query': query,
              }
    context = RequestContext(request, context)
    return render_to_response('feels/display.html', context)