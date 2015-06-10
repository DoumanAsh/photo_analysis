# -*- coding: utf-8 -*-
import av_tracer as trace


@trace.enter
def detectMultiScale(im, casc, scale=1.1, min_nb=3, fl=0, min_xy=[0, 0], max_xy=[0, 0]):
    cmd = [object_detection, im,
           str(casc),
           str(scale),
           str(min_nb),
           str(fl),
           str(min_xy[0]),
           str(min_xy[1]),
           str(max_xy[0]),
           str(max_xy[1])]

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    out, error = p.communicate()
    return int(out.split()[1])


@trace.enter
def get_keywords(im):
    keywords = []
    cmd = [exiftool, im, "-iptc:keywords"]

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    out, err = p.communicate()

    if len(out) > 0:
        out = out.replace(",", " ")
        keywords = out.split(":")[1].split()
    return keywords


def run_test_cases(logs_path, test_suite, test_set_path):
    os.chdir(test_set_path)

    test_cases = os.path.join(logs_path, "test_cases.txt")
    log = os.path.join(logs_path, "test_log.txt")

    with open(test_cases, "w") as f:
        for tc in sorted(test_suite):
            f.write("{0}_tc{1}".format(os.path.split(logs_path)[1], tc))
            for cascade in sorted(test_suite[tc]):
                f.write('\t{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\n'.format(cascade,
                                                                                      test_suite[tc][cascade][0],
                                                                                      test_suite[tc][cascade][1],
                                                                                      test_suite[tc][cascade][2],
                                                                                      test_suite[tc][cascade][3],
                                                                                      test_suite[tc][cascade][4],
                                                                                      test_suite[tc][cascade][5],
                                                                                      test_suite[tc][cascade][6],
                                                                                      test_suite[tc][cascade][7],
                                                                                      test_suite[tc][cascade][8]))

    for image in os.listdir(path):
        base, ext = os.path.splitext(image)
        if ext.lower() != '.jpg':
            continue
        f = open(log, "a")
        print('{0}\t'.format(image))
        f.write('{0}\t'.format(image))
        kw = get_keywords(image)

        for tc in sorted(test_suite):
            found = False
            for cascade in sorted(test_suite[tc]):
                if not test_suite[tc][cascade][0]:
                    continue
                verification_keyword = test_suite[tc][cascade][1]
                scale_factor = test_suite[tc][cascade][2]
                min_neighbors = test_suite[tc][cascade][3]
                flags = test_suite[tc][cascade][4]
                min_xy = [test_suite[tc][cascade][5], test_suite[tc][cascade][6]]
                max_xy = [test_suite[tc][cascade][7], test_suite[tc][cascade][8]]

                num_of_obj = detectMultiScale(os.path.join(path, image), os.path.join(haar_path, cascade),
                                              scale_factor, min_neighbors, flags, min_xy, max_xy)
                if num_of_obj:
                    found = True
                    break

            if found:
                if verification_keyword in kw:
                    conclusion = 'PP'
                else:
                    conclusion = 'NF'
            else:
                if verification_keyword in kw:
                    conclusion = 'PF'
                else:
                    conclusion = 'NP'
            line = '{0}\t'.format(conclusion)
            print(line)
            f.write(line)
        f.write('\n')
        f.close()


def run_ts02():
    import test_suite_02 as ts
    test_logs = os.path.join("D:/_test/cascade_test_results_v02/", ts.name)
    if not os.path.isdir(test_logs):
        os.mkdir(test_logs)
    run_test_cases(test_logs, ts.test_cases, path)


def run_ts03():
    import test_suite_03 as ts
    test_logs = os.path.join("D:/_test/cascade_test_results_v02/", test_set_num, ts.name)
    if not os.path.isdir(test_logs):
        os.mkdir(test_logs)
    run_test_cases(test_logs, ts.test_cases, path)


def run_ts04():
    import test_suite_04 as ts
    test_logs = os.path.join("D:/_test/cascade_test_results_v02/", test_set_num, ts.name)
    if not os.path.isdir(test_logs):
        os.mkdir(test_logs)
    run_test_cases(test_logs, ts.test_cases, path)


def run_ts05():
    import test_suite_05 as ts
    test_logs = os.path.join("D:/_test/cascade_test_results_v02/", test_set_num, ts.name)
    if not os.path.isdir(test_logs):
        os.mkdir(test_logs)
    run_test_cases(test_logs, ts.test_cases, path)


def run_ts06():
    import test_suite_06 as ts
    test_logs = os.path.join("D:/_test/cascade_test_results_v02/", test_set_num, ts.name)
    if not os.path.isdir(test_logs):
        os.mkdir(test_logs)
    run_test_cases(test_logs, ts.test_cases, path)


def run_ts07():
    import test_suite_07 as ts
    test_logs = os.path.join("D:/_test/cascade_test_results_v02/", test_set_num, ts.name)
    if not os.path.isdir(test_logs):
        os.mkdir(test_logs)
    run_test_cases(test_logs, ts.test_cases, path)


def run_ts08():
    import test_suite_08 as ts
    test_logs = os.path.join("D:/_test/cascade_test_results_v02/", test_set_num, ts.name)
    if not os.path.isdir(test_logs):
        os.mkdir(test_logs)
    run_test_cases(test_logs, ts.test_cases, path)


def run_ts09():
    import test_suite_09 as ts
    test_logs = os.path.join("D:/_test/cascade_test_results_v02/", test_set_num, ts.name)
    if not os.path.isdir(test_logs):
        os.mkdir(test_logs)
    run_test_cases(test_logs, ts.test_cases, path)


def run_ts10():
    import test_suite_10 as ts
    test_logs = os.path.join("D:/_test/cascade_test_results_v02/", test_set_num, ts.name)
    if not os.path.isdir(test_logs):
        os.mkdir(test_logs)
    run_test_cases(test_logs, ts.test_cases, path)


import exif_jpeg as exif
import os
import subprocess
from config import *
import datetime

ts = {"01": {'haarcascade_frontalface_alt.xml': [True, '_person', '1.1', '8', '0', '40', '40', '0', '0'],
             'haarcascade_fullbody.xml': [True, '_person', '1.1', '8', '0', '30', '60', '0', '0'],
             'haarcascade_profileface.xml': [True, '_person', '1.1', '9', '0', '30', '60', '0', '0'],
             'haarcascade_mcs_upperbody.xml': [True, '_person', '1.1', '12', '0', '40', '40', '0', '0']}}
ts_name = "suite_08_extention"

test_set_num = "01"
path = "D:/_test/control_set_{0}".format(test_set_num)

test_logs = os.path.join("D:/_test/cascade_test_results_v02/", test_set_num, ts_name)
if not os.path.isdir(test_logs):
    os.mkdir(test_logs)
run_test_cases(test_logs, ts, path)

test_set_num = "02"
path = "D:/_test/control_set_{0}".format(test_set_num)

test_logs = os.path.join("D:/_test/cascade_test_results_v02/", test_set_num, ts_name)
if not os.path.isdir(test_logs):
    os.mkdir(test_logs)
run_test_cases(test_logs, ts, path)
