# -*- coding: utf-8 -*-
import subprocess
import json
import tracer as trace
from main_config import *

@trace.enter
def get_keywords(image):

    with open(cascades_json, encoding='utf-8') as f:
        cascades = json.load(f)

    keywords = []
    for cascade in sorted(cascades):
        if not cascades[cascade]['use']:
            continue

        trace.debug('Check with cascade {0}'.format(cascade))

        is_nested_object = 'nested_object' in cascades[cascade].keys()

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

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        out, error = p.communicate()

        trace.debug('Output: {0}'.format(out))

        if int(out.split()[1]) > 0:
            keywords.extend(cascades[cascade]['keywords'])
            if int(out.split()[4]) > 0:
                keywords.extend(cascades[cascade]['nested_object']['keywords'])

    return list(set(keywords))
