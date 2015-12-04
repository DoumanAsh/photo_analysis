from traceback import extract_stack
from os import path

# Initial values for trace filtering
TRACES = {"error"   :True,
          "warning" :True,
          "info"    :True,
          "debug"   :False,
          "enter"   :False}


def set_tracing(trace_name, value):
    TRACES[trace_name] = value

def info(text):
    if not TRACES['info']:
        return
    stack = extract_stack()
    full_file_name_name, line, _, _ = stack[-2]
    print("Info: {0} [{1}:{2}]".format(text, path.basename(full_file_name_name), line))


def error(text):
    if not TRACES['error']:
        return
    stack = extract_stack()
    full_file_name_name, line, _, _ = stack[-2]
    print("Error: {0} [{1}:{2}]".format(text, path.basename(full_file_name_name), line))


def debug(text):
    if not TRACES['debug']:
        return
    stack = extract_stack()
    full_file_name_name, line, _, _ = stack[-2]
    print("Debug: {0} [{1}:{2}]".format(text, path.basename(full_file_name_name), line))


def enter(function):
    def wrapper(*args):
        if not TRACES['enter']:
            return function(*args)
        stack = extract_stack()
        full_file_name_name, line, _, _ = stack[-2]
        print("Enter: {0}{1} [{2}:{3}]".format(function.__name__,
                                               args,
                                               path.basename(full_file_name_name),
                                               line))
        return function(*args)
    return wrapper


def warning(text):
    if not TRACES['warning']:
        return
    stack = extract_stack()
    full_file_name_name, line, _, _ = stack[-2]
    print("Warning: {0} [{1}:{2}]".format(text, path.basename(full_file_name_name), line))

