def function_in_line(line):
    """
    Returns true if 'def' in line.
    """
    if line.replace(' ', '').startswith('def'):
        return True
    else:
        return False


def get_function_name(line):
    """
    Returns name of function from given line..
    """
    import re
    function_name_pattern = re.compile(r"def (\w+)")
    result = function_name_pattern.match(line)
    if result is not None:
        return result.group(1)


def end_of_function(line):
    """
    Returns true if block of function ends.
    """
    return not line.startswith(' ') and not line.startswith('	')


def get_decorators(code, line_number):
    """
    Returns decorators from above function declaration.
    """
    decorators = []
    up_line_number = line_number - 1
    while code[up_line_number].startswith('@'):
        decorators.append(code[up_line_number])
        up_line_number -= 1
    return decorators


def get_source(code):
    """
    Returns import block and tasks.
    """
    import_block = []
    amount_functions = 0
    tasks = []

    for line in code:
        if 'import' in line:
            import_block.append(line)
        if function_in_line(line):
            amount_functions += 1

    while len(tasks) != amount_functions:
        function_name = ""
        function_start_line_number = 0
        function_stop_line_number = 0

        for line_number in xrange(len(code)):
            line = code[line_number]
            if function_in_line(line):
                function_name = get_function_name(line)
                function_start_line_number = line_number
                decorators = get_decorators(code, line_number)
                continue
            if end_of_function(line) and function_start_line_number != line_number and function_start_line_number != 0:
                function_stop_line_number = line_number
                break
            if line_number == len(code) - 1:
                function_stop_line_number = len(code)
                continue
        if function_name == '':
            break
        decorators.reverse()
        decorators_body = ''.join(decorators)
        function_body = ''.join(code[(function_start_line_number):function_stop_line_number])
        tasks.append({'name': function_name, 'body': decorators_body + function_body})
        code = code[function_stop_line_number:]

    return '\n'.join(import_block), tasks
