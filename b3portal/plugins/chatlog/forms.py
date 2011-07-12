from django import forms
from django.utils.translation import ugettext_lazy as _
from djangoui.widgets import uiSplitDateTimeWidget
from b3portal.models import Map

MAP_CHOICES = [(m.name, m.display_name) for m in Map.objects.all()]
MAP_CHOICES.insert(0, ('','-'))

class ChatLogSearch(forms.Form):
    
    name = forms.CharField(max_length=50, label=_('Name/@id'), required=False)
    datefrom = forms.SplitDateTimeField(('%d/%m/%Y',),('%H:%M',),
                                    widget=uiSplitDateTimeWidget(date_format="%d/%m/%Y",
                                                                 show_seconds=False),
                                    label=_('From'),
                                    required=False)
    text = forms.CharField(max_length=50, label=_('Text'), required=False)
    dateto = forms.SplitDateTimeField(('%d/%m/%Y',),('%H:%M',),
                                    widget=uiSplitDateTimeWidget(date_format="%d/%m/%Y",
                                                                 show_seconds=False),
                                    label=_('To'), required=False)
    map = forms.ChoiceField(choices=MAP_CHOICES, required=False, label = _('Map'))
    
    @property
    def datetime_from(self):
        if self.cleaned_data['datefrom']:
            df = self.cleaned_data['datefrom']
            return df.strftime('%d/%m/%Y'), df.strftime('%H:%M')
        else:
            return None, None
        
    @property
    def datetime_to(self):
        if self.cleaned_data['dateto']:
            df = self.cleaned_data['dateto']
            return df.strftime('%d/%m/%Y'), df.strftime('%H:%M')
        else:
            return None, None        