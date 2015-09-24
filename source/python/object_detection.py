# -*- coding: utf-8 -*-
from json import load as json_load
from subprocess import Popen, PIPE
import tracer as trace
from main_config import *

@trace.enter
def get_keywords(image):

    with open(cascades_json, encoding='utf-8') as f:
        cascades = json_load(f)

    keywords = []
    for cascade in sorted(cascades):
        if not cascades[cascade]['use']:
            continue

        trace.debug('Check with cascade {0}'.format(cascade))

        is_nested_object = 'nested_object' in cascades[cascade]

        cmd = [object_detector, image,
               str(cascades[cascade]['cascade_file']),
               str(cascades[cascade]['scale_factor']),
               str(cascades[cascade]['min_neighbors']),
               str(cascades[cascade]['flags']),
               str(cascades[cascade]['min_x']),
               str(cascades[cascade]['min_y']),
               str(cascades[cascade]['max_x']),
               str(cascades[cascade]['max_y']),
               str(int(is_nested_object))]

        if is_nested_object:
            cmd.extend([str(cascades[cascade]['nested_object']['cascade_file']),
                        str(cascades[cascade]['nested_object']['scale_factor']),
                        str(cascades[cascade]['nested_object']['min_neighbors']),
                        str(cascades[cascade]['nested_object']['flags']),
                        str(cascades[cascade]['nested_object']['min_x']),
                        str(cascades[cascade]['nested_object']['min_y']),
                        str(cascades[cascade]['nested_object']['max_x']),
                        str(cascades[cascade]['nested_object']['max_y'])])

        proc = Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        out, _ = proc.communicate()

        trace.debug('Output: {0}'.format(out))

        if int(out.split()[2]) > 0:
            keywords.extend(cascades[cascade]['keywords'])
            if int(out.split()[5]) > 0:
                keywords.extend(cascades[cascade]['nested_object']['keywords'])

    return list(set(keywords))

if __name__ == "__main__":
    from sys import argv
    res = get_keywords(argv[1])
    print("Keywords:")
    if res:
        print(res)
    else:
        print("n/a. Objects not found")
