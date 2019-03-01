from crossplane import lexer


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
