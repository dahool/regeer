import logging
import traceback
from django.conf import settings
from exceptionlogger.models import ExceptionLog

logger = logging.getLogger(__name__)
    
class ExceptionLoggerMiddleware(object):

    def process_exception(self, request, exception):
        try:
            message = 'EXCEPTION:\n%(exep)s\n\nSTACKTRACE:\n%(trace)s\n\nREQUEST:\n%(request)s' % {'request': str(request), 'exep': str(exception), 'trace': traceback.format_exc()}
            if getattr(settings, 'LOG_EXCEPTION_DB', False):
                ExceptionLog.objects.create(request=str(request),
                                            exception=str(exception),
                                            stacktrace=traceback.format_exc())
            else:
                logger.error(message)
        except:
            logger.error("Cannot generate error message");
        return None
        

