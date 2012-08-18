from django.conf.urls.defaults import url, patterns

urlpatterns = patterns(
    'aurora.terminal.views',
    url(r'^terminal/monitor/(\d{1,30})/$', 'monitor', name='terminal_monitor'),
    url(r'^terminal/start/$', 'start', name='terminal_start'),
    url(r'^terminal/send/$', 'send', name='terminal_send'),
    url(r'^terminal/get_log/(\d{1,30})/$', 'get_log', name='terminal_get_log'),
)
