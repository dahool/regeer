from django import forms
from models import Follow
from django.utils.translation import ugettext_lazy as _

class FollowForm(forms.Form):
    reason = forms.CharField(max_length=100, label=_('Reason'))
    
