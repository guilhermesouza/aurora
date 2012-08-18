from django.conf.urls.defaults import include, patterns, url, handler500
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

handler500 = 'cruiser.views.server_error'

from cruiser.views import index, project, task, new_project, stage
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^projects/(?P<project_id>\d+)$', project, name='project'),
    url(r'^projects/new$', new_project, name='new_project'),
    url(r'^tasks/(?P<task_id>\d+)$', task, name='task'),
    url(r'^stages/(?P<stage_id>\d+)$', stage, name='stage'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
