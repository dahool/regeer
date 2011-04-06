from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from common.view.decorators import render
from djangogravatar.profile import UserProfile, ProfileNotFound
from djangogravatar import settings

@login_required
@cache_page(7200) # cache 2 hours
@render('profile/view.html')
def view(request):
    try:
        profile = UserProfile(request.user.email)
    except ProfileNotFound:
        profile = None
    return {'profile': profile, 'gravatarcfg': settings}