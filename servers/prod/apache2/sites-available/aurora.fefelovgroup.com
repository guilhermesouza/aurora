<VirtualHost 127.0.0.1:8080>
    ServerName www.aurora.fefelovgroup.com
    ServerAlias aurora.fefelovgroup.com
    WSGIDaemonProcess aurora.fefelovgroup.com user=www-data group=www-data \
       processes=2 threads=4 maximum-requests=100 display-name=aurora.fefelovgroup.com-wsgi
    WSGIProcessGroup aurora.fefelovgroup.com
    WSGIApplicationGroup aurora.fefelovgroup.com
    WSGIScriptAlias / /web/aurora.fefelovgroup.com/releases/current/aurora.fefelovgroup.com/aurora/aurora/wsgi.py
    WSGIRestrictSignal Off
    WSGIRestrictStdin Off
    WSGIRestrictStdout Off
    
    ErrorLog    /var/log/apache2/aurora.fefelovgroup.com-error.log
    CustomLog   /var/log/apache2/aurora.fefelovgroup.com-access.log combined
    
    Alias /media/ /web/aurora.fefelovgroup.com/releases/current/aurora.fefelovgroup.com/media/
    
    <Directory /web/aurora.fefelovgroup.com/releases/current/aurora.fefelovgroup.com>
        Options FollowSymLinks
        AllowOverride None
        Order allow,deny
        Allow from all
    </Directory>
</VirtualHost>

