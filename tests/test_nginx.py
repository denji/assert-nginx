import io

import pytest
import assert_nginx


@pytest.fixture
def conf():
    return io.StringIO("""
server {
        listen 80;
        listen [::]:80;

        root /var/www/test.com/html;
        index index.html index.htm index.nginx-debian.html;

        server_name test.com www.test.com;

        location / {
                try_files $uri $uri/ =404;
        }
}
""")


def test_nginx(conf):
    tree = assert_nginx.parse_nginx_config(conf)
    assert len(tree) == 1
    server = tree[0]
    assert server['directive'] == 'server'
    port = False
    for stmt in server['block']:
        print(stmt)
        port |= assert_nginx.get_listen_port(stmt)
        if port:
            assert port == 80

