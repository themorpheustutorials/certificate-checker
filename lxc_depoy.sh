#!/bin/sh

if [[ $(/usr/bin/id -u) != "0" ]]; then
  echo "Please run the script as root!"
  exit 1
fi

# require environment variables
if [[ -z ${DOMAIN} || -z ${CF_Token} || -z ${CF_Account_ID} || -z ${CF_Zone_ID} ]]; then
  echo "Missing environemnt variables, check docs!"
  exit 1
fi

echo >/etc/motd

# stop execution on failure
set -e

# install certificate checker
apk add --update --no-cache gcc python3-dev musl-dev jpeg-dev zlib-dev libpq postgresql-dev postgresql-client acme.sh socat git py3-pip nginx
python3 -m pip install psycopg2-binary==2.8.6 Django gunicorn
git clone https://github.com/themorpheustutorials/certificate-checker /opt/certificate-checker

# get certificate using acme dns-01 challenge
mkdir /root/.acme.sh
acme.sh --server "https://acme-v02.api.letsencrypt.org/directory" --set-default-ca
acme.sh --issue --dns dns_cf -d ${DOMAIN}

# adjust nginx config
cat <<EOF > /etc/nginx/conf.d/default.conf
# https://ssl-config.mozilla.org/#server=nginx&version=1.17.7&config=modern&openssl=1.1.1d&guideline=5.6
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    ssl_certificate /root/.acme.sh/${DOMAIN}/fullchain.cer;
    ssl_certificate_key /root/.acme.sh/${DOMAIN}/${DOMAIN}.key;
    ssl_session_timeout 1d;
    ssl_session_cache shared:MozSSL:10m;  # about 40000 sessions
    ssl_session_tickets off;
    # modern configuration
    ssl_protocols TLSv1.3;
    ssl_prefer_server_ciphers off;
    # HSTS (ngx_http_headers_module is required) (63072000 seconds)
    add_header Strict-Transport-Security "max-age=63072000" always;
    # OCSP stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    location / {
        proxy_pass http://127.0.0.1:8000;
    }
    location /static {
        root   /opt/certificate-checker/app/static;
        index  index.html index.htm;
    }
}
EOF

# create certificates service
cat <<EOF > /etc/init.d/certificates
#!/sbin/openrc-run
function start {
  cd /opt/certificate-checker/app

  export SQL_ENGINE=django.db.backends.postgresql
  export SQL_HOST=postgres.the-morpheus.org
  export SQL_PORT=5432
  export SQL_USER=certificates
  export SQL_PASSWORD=Xe+wmW8v*sWnSK*KJ2mLa5NiVg,szp1v
  export SQL_DATABASE=certificates
  export ALLOWED_HOSTS=localhost

  python3 -m gunicorn app.wsgi:application & 2>&1 > /dev/null
}

function stop {
  killall -9 python3
}
EOF
chmod +x /etc/init.d/hedgedoc

cd /opt/certificate-checker/app

# collect static files to be served using nginx
python3 manange.py collectstatic --no-input

# perform database migrations
python3 manange.py migrate

# configure autostart
rc-update add nginx
rc-update add certificates
rc-service nginx start
rc-service certificates start
