from traceback import extract_stack
from os import path

# Initial values for trace filtering
traces = dict(
    error=True,
    warning=True,
    info=True,
    debug=False,
    enter=False)


def set_tracing(trace_name, value):
    traces[trace_name] = value


def info(text):
    if not traces['info']:
        return
    stack = extract_stack()
    full_file_name_name, line, func_name, _ = stack[-2]
    print("Info: {0} [{1}:{2}]".format(text, path.basename(full_file_name_name), line))


def error(text):
    if not traces['error']:
        return
    stack = extract_stack()
    full_file_name_name, line, func_name, _ = stack[-2]
    print("Error: {0} [{1}:{2}]".format(text, path.basename(full_file_name_name), line))


def debug(text):
    if not traces['debug']:
        return
    stack = extract_stack()
    full_file_name_name, line, func_name, _ = stack[-2]
    print("Debug: {0} [{1}:{2}]".format(text, path.basename(full_file_name_name), line))


def enter(fn):
    def wrapper(*args):
        if not traces['enter']:
            return fn(*args)
        stack = extract_stack()
        full_file_name_name, line, func_name, _ = stack[-2]
        print("Enter: {0}{1} [{2}:{3}]".format(fn.__name__, args, path.basename(full_file_name_name), line))
        return fn(*args)
    return wrapper


def warning(text):
    if not traces['warning']:
        return
    stack = extract_stack()
    full_file_name_name, line, func_name, _ = stack[-2]
    print("Enter: to function={0} [{1}:{2}]".format(func_name, path.basename(full_file_name_name), line))
