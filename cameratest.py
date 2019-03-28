#!/usr/bin/python
import os
import sys
from wallaby import *


def main():
    # start of program goes here
    camera_open()
    print "Camera Opened"

    set_a_button_text("ricardo")

    while a_button() == 0:

        # b button pressed, get new frame
        if right_button() == 1:
            status = camera_update()
            print "Camera Update: " + str(status)

            # channel 0 = Mayor
            # channel 1 = Botguy
            mayor_centroid = get_object_centroid(0, 0)
            mayor_center = get_object_center(0, 0)

            botguy_centroid = get_object_centroid(1, 0)
            botguy_center = get_object_center(1, 0)

            mayor_confidence = get_object_confidence(0, 0)
            botguy_confidence = get_object_confidence(1, 0)

            botguy_area = get_object_area(1, 0)
            mayor_area = get_object_area(0, 0)

            print "Mayor Center X: " + str(mayor_center.x)
            print "Mayor Center Y: " + str(mayor_center.y)
            print "Mayor Area: " + str(mayor_area)
            print "Mayor Confidence: " + str(mayor_confidence)
            print "\n"

            print "Botguy Center X: " + str(botguy_center.x)
            print "Botguy Center Y: " + str(botguy_center.y)
            print "Botguy Area: " + str(botguy_area)
            print "Botguy Confidence: " + str(botguy_confidence)
            print "\n"

            min_height = 80

            # middle = 40
            # right = 100
            # cyce through camera frames to get valid frame

    camera_close()

if __name__ == "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(), "w", 0)
    main()
