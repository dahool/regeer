from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='stats_home'),
    url(r'^naders/$', views.he_stats, name='stats_he_list'),
    url(r'^knifers/$', views.kn_stats, name='stats_kn_list'),
    url(r'^flgthief/$', views.mflg_stats, name='stats_fm_list'),
    url(r'^flgrunner/$', views.qflg_stats, name='stats_fq_list'),
)