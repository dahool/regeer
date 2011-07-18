from django import forms
from django.forms import ModelForm
from b3portal.models import Server
from django.utils.translation import ugettext_lazy as _

class ServerForm(ModelForm):
    
    password = forms.RegexField(label=_("Database Password"),
                                widget=forms.widgets.PasswordInput(attrs={'autocomplete':'off'}),
                                required=True,
                                max_length=100,
                                regex=r"^[-!\"#$%&'()*+,./:;<=>?@[\\\]_`{|}~a-zA-Z0-9]+$",
                                error_message = _("Non ascii chars are forbidden."))
    rcon_password = forms.RegexField(label=_("RCON Password"),
                                widget=forms.widgets.PasswordInput(attrs={'autocomplete':'off'}),
                                required=False,
                                max_length=100,
                                regex=r"^[-!\"#$%&'()*+,./:;<=>?@[\\\]_`{|}~a-zA-Z0-9]+$",
                                error_message = _("Non ascii chars are forbidden."))
            
    def clean(self):
        data = self.cleaned_data
        rcon_ip = data['rcon_ip']
        rcon_port = data['rcon_port']
        rcon_pwd = data['rcon_password']
        
        if not (rcon_ip and rcon_port and rcon_pwd) and (rcon_ip or rcon_port or rcon_pwd):
            raise forms.ValidationError(_("All fields are required for RCON access"));
        
        return data
    
    class Meta:
        model = Server
        exclude = ("uuid")
