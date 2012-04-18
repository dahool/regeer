from django.conf import settings
import logging

logger = logging.getLogger('regeer')

class RconHandler:
    
    def __init__(self, **kwargs):
        self._init_console()
        
    def _init_console(self):
        raise NotImplementedError

    def _runCommand(self, command, *args):
        try:
            method = getattr(self.console, self._commands[command])
            method(*args)
        except Exception, e:
            logger.exception(str(e))
            
    def execute(self):
        resp = []
        for k,v in self.form.cleaned_data.items():
            try:
                resp.append(self._runCommand(k, v))
            except Exception, e:
                logger.exception(str(e))    
        
    def get_status(self):
        return self._runCommand('status')