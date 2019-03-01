
def assert_http2(_file, stmt):
    "assert ssl with http2, return True if it's a SSL server."
    if stmt['directive'] == 'listen':
        port = int(stmt['args'][0].split(':')[-1])
        if port == 443:
            assert 'http2' in stmt['args'], \
                "HTTP/2 everywhere : %s #%i" % (_file, stmt['line'])
            return True
    return False


def assert_ssl_protocols(_file, stmt):
    if stmt['directive'] == 'ssl_protocols':
        assert stmt['args'] == ['TLSv1.2'], \
            "Just TLSv1.2 : %s #%i" % (_file, stmt['line'])
        return True
    return False


def assert_ciphers(_file, stmt):
    if stmt['directive'] == 'ssl_ciphers':
        assert stmt['args'] == ["'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256'"], \
            "Just secure ciphers : %s # %i" % (_file, stmt['line'])
        return True
    return False

