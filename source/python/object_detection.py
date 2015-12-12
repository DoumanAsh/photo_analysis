from sys import argv
from json import load as json_load
import cv2
import tracer as trace
from main_config import cascades_json


@trace.enter
def cv2_get_objects(gray, cascade_file, scale_factor, min_neighbors, flags, min_x=0, min_y=0, max_x=0, max_y=0):
    cascade = cv2.CascadeClassifier(cascade_file)

    if min_x <= 0 or min_y <= 0:
        return cascade.detectMultiScale(gray, scale_factor, min_neighbors)
    elif max_x > 0 and max_y > 0 and max_x > min_x and max_y > min_y:
        return cascade.detectMultiScale(gray, scale_factor, min_neighbors, flags, (min_x, min_y), (max_x, max_y))
    else:
        return cascade.detectMultiScale(gray, scale_factor, min_neighbors, flags, (min_x, min_y))

@trace.enter
def get_keywords(image):
    with open(cascades_json, encoding='utf-8') as json_file:
        cascades = json_load(json_file)

    keywords = []
    for cascade in sorted(cascades):
        if not cascades[cascade]['use']:
            continue

        trace.debug('Check with cascade {0}'.format(cascade))

        img = cv2.imread(image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = cv2_get_objects(gray,
                                cascades[cascade]['cascade_file'],
                                cascades[cascade]['scale_factor'],
                                cascades[cascade]['min_neighbors'],
                                cascades[cascade]['flags'],
                                cascades[cascade]['min_x'],
                                cascades[cascade]['min_y'],
                                cascades[cascade]['max_x'],
                                cascades[cascade]['max_y'])

        if faces.__len__():
            keywords.extend(cascades[cascade]['keywords'])
            if 'nested_object' in cascades[cascade]:
                for (x1, y1, x2, y2) in faces:
                    #show face
                    #img = cv2.rectangle(img,(x1,y1),(x1+x2,y1+y2),(255,0,0),2)
                    #roi_color = img[y1:y1+y2, x1:x1+x2]

                    roi_gray = gray[y1:y1+y2, x1:x1+x2]
                    smiles = cv2_get_objects(roi_gray,
                                             cascades[cascade]['nested_object']['cascade_file'],
                                             cascades[cascade]['nested_object']['scale_factor'],
                                             cascades[cascade]['nested_object']['min_neighbors'],
                                             cascades[cascade]['nested_object']['flags'],
                                             cascades[cascade]['nested_object']['min_x'],
                                             cascades[cascade]['nested_object']['min_y'],
                                             cascades[cascade]['nested_object']['max_x'],
                                             cascades[cascade]['nested_object']['max_y'])

                    if smiles.__len__():
                        #show smile
                        #for (ex,ey,ew,eh) in smiles:
                        #    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

                        keywords.extend(cascades[cascade]['nested_object']['keywords'])

            #resize
            #height, width = img.shape[:2]
            #img = cv2.resize(img, (int(height/1.5), int(width/1.2)))

            #show image
            #cv2.imshow('img',img)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()

    return list(set(keywords))

if __name__ == "__main__":
    res = get_keywords(argv[1])
    if res:
        print("Keywords:", ", ".join(res))
    else:
        print("n/a. Objects not found")
