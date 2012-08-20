server {
        listen     80;
        server_name aurora.fefelovgroup.com;
        access_log /var/log/nginx/aurora.fefelovgroup.com.log;
        error_log /var/log/nginx/aurora.fefelovgroup.com-error.log info;
        location / {
                proxy_pass http://127.0.0.1:8080/;
                include /etc/nginx/proxy.conf;
        }
        location /media/ {
                root /web/aurora.fefelovgroup.com/releases/current/aurora.fefelovgroup.com/aurora;
                expires 30d;
        }

}

