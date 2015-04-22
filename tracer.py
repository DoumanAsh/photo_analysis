import traceback
import os

# Initial values for trace filtering
from main_config import traces


def set_tracing(trace_name, value):
    traces[trace_name] = value


def info(text):
    if not traces['info']:
        return
    stack = traceback.extract_stack()
    full_file_name, line, func_name, unused = stack[-2]
    path, file = os.path.split(full_file_name)
    print("Info: {0} [{1}:{2}]".format(text, file, line))


def error(text):
    if not traces['error']:
        return
    stack = traceback.extract_stack()
    full_file_name, line, func_name, unused = stack[-2]
    path, file = os.path.split(full_file_name)
    print("Error: {0} [{1}:{2}]".format(text, file, line))


def debug(text):
    if not traces['debug']:
        return
    stack = traceback.extract_stack()
    full_file_name, line, func_name, unused = stack[-2]
    path, file = os.path.split(full_file_name)
    print("Debug: {0} [{1}:{2}]".format(text, file, line))


def enter(fn):
    def wrapper(*args):
        if not traces['enter']:
            return fn(*args)
        stack = traceback.extract_stack()
        full_file_name, line, func_name, unused = stack[-2]
        path, file = os.path.split(full_file_name)
        print("Enter: {0}{1} [{2}:{3}]".format(fn.__name__, args, file, line))
        return fn(*args)
    return wrapper


def warning(text):
    if not traces['warning']:
        return
    stack = traceback.extract_stack()
    full_file_name, line, func_name, unused = stack[-2]
    path, file = os.path.split(full_file_name)
    print("Enter: to function={0} [{1}:{2}]".format(func_name, file, line))