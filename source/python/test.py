import os
import object_detection

path = "D:\_test\control_set_01_02_positive"

number_of_images = 0
detected = 0

for file in os.listdir(path):
    with open("test_res.txt", "w") as f:
        number_of_images += 1
        if "люди" in object_detection.get_keywords(os.path.join(path, file)):
            detected += 1
        print("{0} % detected ({1} from {2})".format(int(detected/number_of_images*1000)/10, detected, number_of_images))
        f.write("{0}\t{1}\t{2}\n".format(int(detected/number_of_images*1000)/10, detected, number_of_images))