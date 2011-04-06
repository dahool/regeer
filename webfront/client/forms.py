from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.validators import EMPTY_VALUES

TIME_CHOICES = (
    ('m', _('Minutes')),
    ('h', _('Hours')),
    ('d', _('Days')),
    ('w', _('Weeks')),
    ('M', _('Month')),
    ('y', _('Years')),
)

class NoticeForm(forms.Form):
    
    reason = forms.CharField(max_length=765, label=_('Reason'))

    class Meta:
        type = 1

class PenaltyForm(NoticeForm):
    
    permanent = forms.BooleanField(label=_('Permanent'), required=False) 
    time = forms.IntegerField(min_value=1, label=_('Duration'), required=False)
    time_type = forms.ChoiceField(label=_('Period'), choices=TIME_CHOICES)

    def clean_time(self):
        time = self.cleaned_data['time']
        if time in EMPTY_VALUES and not self.cleaned_data['permanent']:
            raise ValidationError(self.fields['time'].error_messages['required'])
        return time

    class Meta:
        type = 2