from django.http import HttpResponse
from django.shortcuts import render

def index(request):
  context = {}
  # if this is a POST request we need to process the form data
  if request.method == 'POST':
      # create a form instance and populate it with data from the request:
      form = NameForm(request.POST)
      # check whether it's valid:
      if form.is_valid():
          # process the data in form.cleaned_data as required
          # ...
          # redirect to a new URL:
          cd = form.cleaned_data
          cd
          return HttpResponseRedirect('feels/display.html')

  # if a GET (or any other method) we'll create a blank form
  else:
      form = NameForm()

  return render(request, 'feels/index.html', context)

def display(request):
  context = {}
  return render(request, 'feels/display.html', context)