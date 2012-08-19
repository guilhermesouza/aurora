from django.conf.urls import include, patterns, url, handler500
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.views import login, logout
admin.autodiscover()

handler500 = 'cruiser.views.server_error'

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, {'next_page': '/'}, name='logout', ),
)

urlpatterns += patterns(
    'aurora.cruiser.views',
    url(r'^$', 'index', name='index'),
    url(r'^project/(?P<project_id>\d+)$', 'project', name='project'),
    url(r'^project/new$', 'new_project', name='new_project'),
    url(r'^task/(?P<task_id>\d+)$', 'task', name='task'),
    url(r'^task/new$', 'new_task', name='new_task'),
    url(r'^stage/(?P<stage_id>\d+)$', 'stage', name='stage'),
    url(r'^stage/(?P<stage_id>\d+)/(?P<task_id>\d+)/exec$', 'exec_task', name='exec_task'),
    url(r'^stage/new$', 'new_stage', name='new_stage'),
    url(r'^deployment/(?P<deploy_id>\d+)/$', 'monitor', name='deployment_monitor'),
    url(r'^deployment/(?P<deploy_id>\d+)/send/$', 'send', name='send_to_deployment'),
    url(r'^deployment/(?P<deploy_id>\d+)/get_log/$', 'get_log', name='deployment_log'),
    url(r'^deployment/(?P<deploy_id>\d+)/cancel/$', 'cancel', name='cancel_deployment'),
)

urlpatterns += staticfiles_urlpatterns()
