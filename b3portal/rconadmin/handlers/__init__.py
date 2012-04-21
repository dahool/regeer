from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
import logging
from django.utils.encoding import force_unicode
from django.utils.translation import gettext as _

logger = logging.getLogger('regeer')

def find_handler_for_game(game):
    try:
        handler = settings.RCON_HANDLERS[game]
    except KeyError:
        return None
    try:
        mod, classname = ".".join(handler.split('.')[:-1]), handler.split('.')[-1]
        mod = __import__(mod, globals(), locals(), [classname])
        func = getattr(mod, classname)
    except:
        logger.exception(game)
        return None
    return func
    
class RconForm(forms.Form):

    def __init__(self, *args, **kwargs):
        data = kwargs.pop('data', None)
        if args: data = args[0]
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
            field = self.fields[name]
            if '' == value and not field.blank:
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
                r = self._runCommand(k, force_unicode(v))
                if not r or r == '': r = _('Success.')
                resp.append(r)
            except Exception, e:
                logger.exception(str(e))
                resp.append(str(e))    
        return resp
    
    def get_status(self):
        raise NotImplementedError
    
class Q3ARconHandler(RconHandler):

    def get_status(self):
        map = self.console.getMap()
        clients = self.console.getClients()
        return (map, clients)