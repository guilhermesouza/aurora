def get_source(code):
    import_block = []
    tasks = []

    for line in code:
        if 'import' in line:
            import_block.append(line)

    parts = ''.join(code).split('def')[1:]
    for part in parts:
        def_name = part.split('(')[0].replace(' ', '')
        tasks.append({'name': def_name, 'body': "def" + part})

    return '\n'.join(import_block), tasks
