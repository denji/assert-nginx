from crossplane import lexer


"""

        it = lexer._lex_file_object(io.StringIO(ff.content_string))
        it = lexer._balance_braces(it)
        tree = parse(it)
        for root in tree:
            print(root['directive'], root['args'])
            if root['directive'] != 'server':
                continue
            has_ssl_protocol = False
            is_ssl = False
            has_ciphers = False
            for stmt in root['block']:
                print("  ", stmt)
                is_ssl |= assert_http2(site, stmt)
                if is_ssl:
                    has_ssl_protocol |= assert_ssl_protocols(site, stmt)
                    has_ciphers |= assert_ciphers(site, stmt)
            if is_ssl:
                assert has_ssl_protocol
                assert has_ciphers


"""


def parse_nginx_config(config):
    """
    Config is something readable, open('my_config', 'r') or
    io.StringIO(my_config_as string)

    return lots of parenthesis
    """
    it = lexer._lex_file_object(config)
    it = lexer._balance_braces(it)
    return parse(it)


def parse(tokens, level=0):
    commands = []
    stack = []
    for token, line, quoted in tokens:
        if token == "}" and not quoted:
            break
        if token == "{" and not quoted:
            #print(level * " ", stack)
            block = parse(tokens, level+1)
            stmt = dict(directive=stack[0], args=stack[1:], block=block, line=line)
            commands.append(stmt)
            stack = []
            continue
        directive = token
        if directive.startswith('#') and not quoted:
            continue
        stack.append(directive)
        if directive == ';' and not quoted:
            #print(level * " ", stack)
            stmt = dict(directive=stack[0], args=stack[1:-1], line=line)
            commands.append(stmt)
            stack = []
    return commands


def get_listen_port(stmt):
    if stmt['directive'] == 'listen':
        return int(stmt['args'][0].split(':')[-1])
    return False
