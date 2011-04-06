from django.http import Http404
from django.shortcuts import _get_queryset

def get_object_or_404(klass, *args, **kwargs):
    try:
        using = kwargs.pop('using')
    except:
        using = None
    queryset = _get_queryset(klass)
    try:
        if using:
            queryset._db = using
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        raise Http404('No %s matches the given query.' % queryset.model._meta.object_name)