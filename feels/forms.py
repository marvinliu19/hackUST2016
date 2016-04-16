from django import forms

class QueryForm(forms.Form):
    query_text = forms.CharField(label='', max_length=100)