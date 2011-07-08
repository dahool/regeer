from django import forms
from django.forms import ModelForm
from b3portal.models import Server
from django.utils.translation import ugettext_lazy as _

class ServerForm(ModelForm):
    
    pwd = forms.RegexField(label=_("Database Password"),
                                widget=forms.widgets.PasswordInput(attrs={'autocomplete':'off'}),
                                required=False,
                                max_length=100,
                                regex=r"^[-!\"#$%&'()*+,./:;<=>?@[\\\]_`{|}~a-zA-Z0-9]+$",
                                error_message = _("Non ascii chars are forbidden."),
                                initial='')
        
    class Meta:
        model = Server
        exclude = ("password", "slug")

    def save(self, commit=True):
        s = super(ServerForm, self).save(commit=False)
        rp = self.cleaned_data['pwd']
        if rp and rp <> '':
            s.set_password(rp)
        if commit:
            s.save()
            self.save_m2m()
        return s