# -*- coding: utf-8 -*-
import tracer as trace


def get_data_from_image(image, option):
    from main_config import exiftool
    import subprocess
    import json
    '''
    cmd1 = [exiftool]
    cmd1.extend('-tagsfromfile @ -iptc:all -codedcharacterset=utf8 -charset iptc=cp1251'.split())
    cmd1.append(image)
    p = subprocess.Popen(cmd1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    out, err = p.communicate()
    '''
    options = ['-j', '-g', str(image), str(option)]

    cmd = [exiftool]
    cmd.extend(options)

    trace.debug('Cmd: {0}'.format(cmd))

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    out, err = p.communicate()
    trace.debug('stdout: {0}; stderr: {1}'.format(out, err))

    return json.loads(out[1:-2])
