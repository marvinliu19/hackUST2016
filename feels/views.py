from django.http import HttpResponse
from django.shortcuts import render

def index(request):
  context = {}
  return render(request, 'feels/index.html', context)

def results(request):
  response = "Your query was"
  return HttpResponse(response)