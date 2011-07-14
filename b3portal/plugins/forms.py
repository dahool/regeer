from django import forms

class NoValuePluginForm(forms.Form):
    enabled = forms.BooleanField()
    
class ValuePluginForm(NoValuePluginForm):
    value = forms.CharField(max_length=500)