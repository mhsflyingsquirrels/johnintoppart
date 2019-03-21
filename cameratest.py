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

            # channel 0 = red
            # channel 1 = yellow
            red_centroid = get_object_centroid(0, 0)
            red_center = get_object_center(0, 0)

            yellow_centroid = get_object_centroid(1, 0)
            yellow_center = get_object_center(1, 0)

            red_confidence = get_object_confidence(0, 0)
            yellow_confidence = get_object_confidence(0, 0)

            yellow_area = get_object_area(1, 0)
            red_area = get_object_area(0, 0)

            print "Red Center X: " + str(red_center.x)
            print "Red Center Y: " + str(red_center.y)
            print "Red Area: " + str(red_area)
            print "Red Confidence: " + str(red_confidence)
            print "\n"

            print "Yellow Center X: " + str(yellow_center.x)
            print "Yellow Center Y: " + str(yellow_center.y)
            print "Yellow Area: " + str(yellow_area)
            print "Yellow Confidence: " + str(yellow_confidence)

            # cyce through camera frames to get valid frame

    camera_close()

if __name__ == "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(), "w", 0)
    main()
