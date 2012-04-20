from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
import logging
from django.utils.encoding import force_unicode

logger = logging.getLogger('regeer')

class RconForm(forms.Form):

    def __init__(self, *args, **kwargs):
        data = kwargs.pop('data', args[0])
        if data:
            cmd = data['cmd']
            value = data['data']
            data = {cmd: value}
        super(RconForm, self).__init__(data, **kwargs)
    
    def clean(self):
        #cleaned_data = super(RconForm, self).clean()
        #cleaned_data contains all fields, we want to keep only the valid ones
        data = self.data
        for name, value in data.items():
            if name not in self.fields.keys():
                raise forms.ValidationError(_("Unknown command."))
            if '' == value:
                field = self.fields[name]
                raise forms.ValidationError(field.error_messages['invalid'])
        return data
    
class RconHandler:
    
    def __init__(self, server, data):
        self._init_console()
        
    def _init_console(self):
        raise NotImplementedError

    def _runCommand(self, command, *args):
        try:
            method = getattr(self.console, self._commands[command])
            return method(*args)
        except Exception, e:
            logger.exception(str(e))
            
    def execute(self):
        if not self.form.is_valid():
            errors = []
            for field, message in self.form.errors.items():
                errors.append(message.as_text())
            raise ValidationError(', '.join(errors))
        
        resp = []
        for k,v in self.form.cleaned_data.items():
            try:
                logger.debug("Sending %s %s" % (k, v))
                resp.append(self._runCommand(k, force_unicode(v)))
            except Exception, e:
                logger.exception(str(e))    
        return resp
    
    def get_status(self):
        return self._runCommand('status')