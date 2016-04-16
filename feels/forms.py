from django import forms

class QueryForm(forms.Form):
    query_text = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'@kanyewest'}))