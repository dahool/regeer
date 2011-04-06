from common.decorators import permission_required_with_403

from django.http import HttpResponseRedirect

@permission_required_with_403('autoslap.view_autoslap')
def home(request):
    return HttpResponseRedirect("/");