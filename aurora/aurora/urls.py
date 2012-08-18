from django.conf.urls.defaults import include, patterns, url, handler500
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

handler500 = 'cruiser.views.server_error'

from cruiser.views import index, project
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^projects/(\d{4})$', project, name='project'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
