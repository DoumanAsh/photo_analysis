# -*- coding: utf-8 -*-
import exif_jpeg as exif
import av_tracer as trace
import os
import subprocess
from config import *
import datetime

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
    cmd = [exiftool]
    cmd.append(image)
    cmd.append("-iptc:keywords")
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    out, err = p.communicate()

    if len(out) > 0:
        out = out.replace(",", " ")
        keywords = out.split(":")[1].split()
    return keywords

path = "D:/_test/control_set_02"

cascades = [os.path.join(haar_path, 'haarcascade_frontalface_alt.xml'),
            os.path.join(haar_path, 'haarcascade_fullbody.xml')]

os.chdir(path)
negative_passed = 0
positive_passed = 0
negative_failed = 0
positive_failed = 0

verification_keyword = "_person"
scale_factor = 1.1
min_neighbors = 8
flags = 0
min_x = 40
min_y = 40
max_x = 0
max_y = 0

start_time = datetime.datetime.now()
results_fn = "D:/_test/cascade_test_results_v01/test_{0}_summary.log".format(start_time.strftime("%Y-%m-%d_%H-%M-%S"))
test_log = "D:/_test/cascade_test_results_v01/test_{0}_log.log".format(start_time.strftime("%Y-%m-%d_%H-%M-%S"))

with open(results_fn, "w") as f:
    f.write('Date/time: {0}\n'.format(start_time.strftime("%Y-%m-%d %H:%M:%S")))
    f.write('===========================\n'
            'Verification keyword: "{0}"\n'
            'Test set: {1}\n'.format(verification_keyword, path))
    f.write('===========================\nCascades:\n---------------------------\n')
    for cascade in cascades:
        f.write('{0}\n'.format(os.path.split(cascade)[1]))
    f.write('===========================\nSettings of detectMultiScale:\n---------------------------\n')
    f.write("scale_factor {0}\nmin_neighbors {1}\nflags {2}\n"
            "min_size ({3}, {4})\n"
            "max_size ({5}, {6})\n".format(scale_factor, min_neighbors, flags, min_x, min_y, max_x, max_y))

    f.write('===========================\n'
            'Test log: {0}\n'
            '---------------------------\n'.format(test_log))
    for image in os.listdir(path):
        base, ext = os.path.splitext(image)
        if ext != ".jpg":
            continue

        kw = get_keywords(image)

        found = False
        for cascade in cascades:
            num_of_obj = detectMultiScale(os.path.join(path, image), cascade, scale_factor, min_neighbors, flags, [min_x, min_y])
            if num_of_obj:
                found = True
                break

        conclusion = ''
        if found:
            if verification_keyword in kw:
                conclusion = 'positive PASSED'
                positive_passed += 1
            else:
                conclusion = 'negative FAILED'
                negative_failed += 1
        else:
            if verification_keyword in kw:
                conclusion = 'positive FAILED'
                positive_failed += 1
            else:
                conclusion = 'negative PASSED'
                negative_passed += 1
        line = '{0} {1} "{2}"\n'.format(conclusion, image, kw)
        print(line)
        ff = open(test_log, "a")
        ff.write(line)
    pos_t = positive_passed + positive_failed
    neg_t = negative_passed + negative_failed
    total = pos_t + neg_t
    pos_p = positive_passed/pos_t  # positive passed %
    pos_f = 1 - pos_p  # positive failed %
    neg_p = negative_passed/neg_t  # negative passed %
    neg_f = 1 - neg_p  # negative failed %
    tot_p = (positive_passed + negative_passed)/total  # total passed %
    tot_f = 1 - tot_p  # total passed %

    res_text = '''
===========================
Results:
---------------------------
Total: {0}
Negative: passed: {1}; failed {2}
Positive: passed: {3}; failed {4}
'''.format(total, negative_passed, negative_failed, positive_passed, positive_failed)
    print(res_text)
    f.write(res_text)

    summary = '''
===========================
Summary:
---------------------------
pos_t neg_t pos_p pos_f neg_p neg_f pos_p% pos_f% neg_p% neg_f% tot_p% tot_f% test_set ver_kw
{0}  {1}    {2}   {3}   {4}   {5}   {6}    {7}    {8}    {9}    {10}   {11}   {12}     {13}
'''.format(pos_t,
           neg_t,
           positive_passed,
           positive_failed,
           negative_passed,
           negative_failed,
           pos_p,
           pos_f,
           neg_p,
           neg_f,
           tot_p,
           tot_f,
           path,
           verification_keyword)

    f.write(summary)