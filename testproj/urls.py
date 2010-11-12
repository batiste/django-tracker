from django.conf.urls.defaults import *
from tracker.views import track, report, get_stats, test

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^testproj/', include('testproj.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
    (r'^test/', test),
    (r'^track/', track),
    (r'^report/', report),
    (r'^get_stats/', get_stats),
)
