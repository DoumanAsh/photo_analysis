# -*- coding: utf-8 -*-
name = "suite_04"

test_cases = {
#                                          Use    Keyword   ScaleF MinNeigh Flag MinX  MinY  MaxX MaxY
"01": {'haarcascade_frontalface_alt.xml': [True, '_person', '1.1', '10',    '0', '10', '10', '0', '0'],
       'haarcascade_fullbody.xml'       : [True, '_person', '1.1', '10',    '0', '7' , '15', '0', '0'],
       'haarcascade_profileface.xml'    : [True, '_person', '1.1', '10',    '0', '10', '10', '0', '0'],
       'haarcascade_upperbody.xml'      : [True, '_person', '1.1', '10',    '0', '10', '15', '0', '0']},
"02": {'haarcascade_frontalface_alt.xml': [True, '_person', '1.1', '10',    '0', '20', '20', '0', '0'],
       'haarcascade_fullbody.xml'       : [True, '_person', '1.1', '10',    '0', '15', '30', '0', '0'],
       'haarcascade_profileface.xml'    : [True, '_person', '1.1', '10',    '0', '20', '20', '0', '0'],
       'haarcascade_upperbody.xml'      : [True, '_person', '1.1', '10',    '0', '20', '30', '0', '0']},
"03": {'haarcascade_frontalface_alt.xml': [True, '_person', '1.1', '10',    '0', '40', '40', '0', '0'],
       'haarcascade_fullbody.xml'       : [True, '_person', '1.1', '10',    '0', '30', '60', '0', '0'],
       'haarcascade_profileface.xml'    : [True, '_person', '1.1', '10',    '0', '40', '40', '0', '0'],
       'haarcascade_upperbody.xml'      : [True, '_person', '1.1', '10',    '0', '40', '60', '0', '0']},
"04": {'haarcascade_frontalface_alt.xml': [True, '_person', '1.1', '10',    '0', '60', '60', '0', '0'],
       'haarcascade_fullbody.xml'       : [True, '_person', '1.1', '10',    '0', '45', '90', '0', '0'],
       'haarcascade_profileface.xml'    : [True, '_person', '1.1', '10',    '0', '60', '60', '0', '0'],
       'haarcascade_upperbody.xml'      : [True, '_person', '1.1', '10',    '0', '60', '90', '0', '0']},
"05": {'haarcascade_frontalface_alt.xml': [True, '_person', '1.1', '10',    '0', '80', '80', '0', '0'],
       'haarcascade_fullbody.xml'       : [True, '_person', '1.1', '10',    '0', '60', '120', '0', '0'],
       'haarcascade_profileface.xml'    : [True, '_person', '1.1', '10',    '0', '80', '80', '0', '0'],
       'haarcascade_upperbody.xml'      : [True, '_person', '1.1', '10',    '0', '80', '120', '0', '0']},
"06": {'haarcascade_frontalface_alt.xml': [True, '_person', '1.1', '10',    '0', '100', '100', '0', '0'],
       'haarcascade_fullbody.xml'       : [True, '_person', '1.1', '10',    '0', '75' , '150', '0', '0'],
       'haarcascade_profileface.xml'    : [True, '_person', '1.1', '10',    '0', '100', '100', '0', '0'],
       'haarcascade_upperbody.xml'      : [True, '_person', '1.1', '10',    '0', '100', '150', '0', '0']}
}