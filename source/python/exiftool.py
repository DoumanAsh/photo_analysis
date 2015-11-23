import tracer as trace
from main_config import exiftool
from subprocess import Popen, PIPE
from json import loads as json_loads


def get_data_from_image(image, option):
    cmd = [exiftool, '-j', '-g', '-charset', 'exiftool=Russian', str(option), str(image)]

    trace.debug('Cmd: {0}'.format(cmd))

    proc = Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    out, err = proc.communicate()
    trace.debug('stdout: {0}; stderr: {1}'.format(out, err))

    return json_loads(out[1:-2])


def write_iptc_tags_to_image(image, iptc_dict):
    cmd = [exiftool,
           '-codedcharacterset=UTF8',
           '-charset',
           'iptc=Russian',
           '-charset', 'filename=Russian']

    for item in iptc_dict:
        if item == "keywords":
            for kw in iptc_dict[item]:
                cmd.append("-iptc:{0}-={1}".format(item, kw))
                cmd.append("-iptc:{0}+={1}".format(item, kw))
        else:
            cmd.append("-iptc:{0}={1}".format(item, iptc_dict[item]))

    cmd.append(str(image))

    trace.debug('Cmd: {0}'.format(cmd))

    proc = Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    out, err = proc.communicate()
    trace.debug('stdout: {0}; stderr: {1}'.format(out, err))
