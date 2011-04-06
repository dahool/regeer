import datetime
from time import mktime
from django.db import models
from django.contrib.admin.filterspecs import FilterSpec
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _

class DateIntFieldFilterSpec(FilterSpec):
    def __init__(self, f, request, params, model, model_admin):
        super(DateIntFieldFilterSpec, self).__init__(f, request, params, model, model_admin)

        self.field_generic = '%s__' % self.field.name

        self.date_params = dict([(k, v) for k, v in params.items() if k.startswith(self.field_generic)])

        today = datetime.datetime.today()
        today_start = today.replace(hour=0,minute=0,second=0).timetuple()
        today_end = today.replace(hour=23,minute=59,second=59).timetuple()
        
        last_hour = (today - datetime.timedelta(hours=1)).timetuple()
        last_10_minutes = (today - datetime.timedelta(minutes=10)).timetuple()
        last_30_minutes = (today - datetime.timedelta(minutes=30)).timetuple()


        self.links = (
            (_('Any date'), {}),
            (_('Today'), {'%s__gte' % self.field.name: str(int(mktime(today_start))),
                             '%s__lte' % f.name: str(int(mktime(today_end)))}),
            (_('Last 10 minutes'), {'%s__gte' % self.field.name: str(int(mktime(last_10_minutes)))}),
            (_('Last 30 minutes'), {'%s__gte' % self.field.name: str(int(mktime(last_30_minutes)))}),
            (_('Last hour'), {'%s__gte' % self.field.name: str(int(mktime(last_hour)))}),
        )

    def title(self):
        return self.field.verbose_name

    def choices(self, cl):
        for title, param_dict in self.links:
            yield {'selected': self.date_params == param_dict,
                   'query_string': cl.get_query_string(param_dict, [self.field_generic]),
                   'display': title}
