#!/usr/bin/python
import os
import sys
from wallaby import *

KP = 5
SPINDLE_MOTOR = 0
SIDE_TOWER_EXTEND_AMNT = -5300
MIDDLE_TOWER_EXTEND_AMNT = -11200
DROP_EXTEND_AMNT = -2000

BLACK_THRESH = 1500

MOVEMENT_DEBUG = True

SPEED_COMPENSATION = 26


class CreateLibrary:

    def __init__(self):
        self.print_value = None

    # function to print values to console without repeating values
    def smart_print(self, string, value):
        if self.print_value != value and MOVEMENT_DEBUG is True:
            print string + str(value)
        elif not MOVEMENT_DEBUG:
            print value

        print "",
        self.print_value = value

    def cliff_line_follow(self, distance, speed, thresh):
        set_create_distance(0)

        while -get_create_distance() < distance:
            if get_create_lfcliff_amt() < thresh:
                create_drive_direct(speed, speed / 2)
            elif get_create_lfcliff_amt() > thresh:
                create_drive_direct(speed / 2, speed)

            self.smart_print("Distance: ", get_create_distance())

        create_stop()

    # bad programming
    def rcliff_not_front_line_follow(self, distance, speed, thresh):
        set_create_distance(0)

        while -get_create_distance() < distance:
            if get_create_rcliff_amt() < thresh:
                create_drive_direct(speed, speed / 2)
            elif get_create_rcliff_amt() > thresh:
                create_drive_direct(speed / 2, speed)

            self.smart_print("Distance: ", get_create_distance())

    def drive_arc(self, speed, radius, distance):
        create_drive(speed, radius)

        while -get_create_distance() < distance:
            self.smart_print("Arc Distance: ", get_create_distance())

        create_stop()

    # go backward for certain distance + speed
    def backward_for(self, distance, speed):
        set_create_distance(0)
        create_drive_straight(-speed)

        while get_create_distance() < distance:
            measured_distance = get_create_distance()
            self.smart_print("Distance: ", measured_distance)

        create_stop()

    # go forward for certain distance + speed (Forward = bumper)
    def forward_for(self, distance, speed):
        set_create_distance(0)
        create_drive_direct(speed, speed+SPEED_COMPENSATION)

        while -get_create_distance() < distance:
            self.smart_print("Distance: ", get_create_distance())

        create_stop()

    # only works on the right wall
    def wall_follow(self, distanceFromWall, speed):
        error = get_create_wall_amt() - distanceFromWall
        self.smart_print("Error: ", error)

        turnRadius = error * KP

        if get_create_wall_amt() != distanceFromWall:
            create_drive(speed, turnRadius)
        else:
            backward_for(2, speed)

    # positive is clockwise
    def turn_for(self, angle, speed):
        set_create_normalized_angle(0)

        if angle > 0:  # clockwise
            print "spinning clockwise"
            create_spin_CW(speed)

            while get_create_normalized_angle() > -angle:
                self.smart_print("Angle: ", get_create_normalized_angle())

        elif angle < 0:
            print "spinnng counter clockwise"
            create_spin_CCW(speed)

            while -get_create_normalized_angle() > angle:
                self.smart_print("Angle: ", get_create_normalized_angle())

        create_stop()

    def turn_motor_to_tick(self, motor, incr, tick):

        print "IM TURNING THE MOTOR RIGHT NOW"
        mrp(motor, incr, tick)
        msleep(100)

        # dumb
        block_motor_done(motor)

    def forward_until_bumper(self, speed, both=True):
        create_drive_direct(speed, speed)

        print "Waiting for bump"
        if both is True:
            while get_create_lbump() == 0 and get_create_lbump() == 0:
                msleep(5)

        else:
            while get_create_lbump() == 0 or get_create_lbump() == 0:
                msleep(5)

        print "Bump detected"
        create_stop()

    def gradual_servo(self, servo, pos, speed):
        x = get_servo_position(servo)

        while get_servo_position(servo) != pos:
            set_servo_position(servo, x)
            msleep(speed)

            # figure out whether to increment or decrement servo
            if x > pos:
                x -= 1
            else:
                x += 1

            print "servo tick: " + str(x)

    def bad_motor(self, port, time, power):
        motor(port, power)
        msleep(time)
        ao()

    def wall_follow_till(self, distance, speed, condition_check, condition, forwards=True):
        status = "None"
        while condition_check() == 0 or condition_check() > condition:
            if forwards:
                if get_create_wall_amt() < distance:
                    create_drive_direct(speed, speed / 2)
                elif get_create_wall_amt() > distance:
                    create_drive_direct(speed / 2, speed)
                else:
                    create_drive_direct(speed, speed)
            else:
                if get_create_wall_amt() < 10:
                    if status == "RIGHT":
                        create_drive_direct(-speed / 2, -speed)
                    elif status == "LEFT":
                        create_drive_direct(-speed, -speed / 2)
                    else:
                        create_drive_direct(-speed, -speed / 2)

                elif get_create_wall_amt() > distance:
                    create_drive_direct(-speed, -speed / 2)
                    status = "RIGHT"
                    print "turning right"
                elif get_create_wall_amt() < distance:
                    create_drive_direct(-speed / 2, -speed)
                    status = "LEFT"
                    print "turning left"
                else:
                    create_drive_direct(-speed, -speed)
                    status = "STRAIGHT"
                    print "straight"

            self.smart_print(string="Condition: ", value=condition_check())
            print get_create_wall_amt()

        self.stop()

    def stop(self):
        create_stop()

    def get_both_bumpers(self):
        return get_create_lbump() or get_create_rbump()


def get_tower_pos():
    print "Entering tower pos grabbing function"

    camera_open()

    # middle = 40
    # right = 100
    # cyce through camera frames to get valid frame
    MIN_HEIGHT = 100
    MIDDLE = 40
    RIGHT = 100

    buffer_int = 0

    while buffer_int < 20:
        buffer_int += 1
        camera_update()

    status = camera_update()
    print "Camera Update: " + str(status)

    # channel 0 = Mayor
    # channel 1 = Botguy
    mayor_center = get_object_center(0, 0)
    botguy_center = get_object_center(1, 0)

    botguy_status = "UNKNOWN"
    mayor_status = "UNKNOWN"

    print "Botguy X: " + str(botguy_center.x)
    print "Botguy Y: " + str(botguy_center.y)
    print "Mayor X: " + str(mayor_center.x)
    print "Mayor Y: " + str(mayor_center.y)

    #  make sure that object is found
    if botguy_center.x > -1:
        # if botguy_center.y < MIN_HEIGHT:
        if botguy_center.x < MIDDLE:
            botguy_status = "LEFT"
        elif botguy_center.x < RIGHT:
            botguy_status = "MID"
        elif botguy_center.x > RIGHT:
            botguy_status = "RIGHT"

    if mayor_center.x > -1:
        # if mayor_center.y < MIN_HEIGHT:
        if mayor_center.x < MIDDLE:
            mayor_status = "LEFT"
        elif mayor_center.x < RIGHT:
            mayor_status = "MID"
        elif mayor_center.x > RIGHT:
            mayor_status = "RIGHT"

    camera_close()

    return botguy_status, mayor_status

def get_right_tower(create):
    # -7124
    move_to_position(SPINDLE_MOTOR, 800, SIDE_TOWER_EXTEND_AMNT)
    create.forward_for(30, 100)
    msleep(100)
    create.turn_for(7, 100)
    msleep(100)
    create.forward_for(10, 100)
    msleep(100)

    # the claw should be ready to grab now

    # return back to starting area
    create.turn_for(-65, 100)
    msleep(100)
    create.forward_for(25, 100)
    msleep(100)

    # being realignment process
    create.turn_for(-20, 100)
    create.forward_until_bumper(100)
    msleep(100)
    create.backward_for(2, 100)
    msleep(100)
    create.turn_for(-40, 100)


def get_middle_tower(create):
    move_to_position(SPINDLE_MOTOR, 800, MIDDLE_TOWER_EXTEND_AMNT)
    create.forward_for(20, 100)
    msleep(100)
    create.turn_for(-3, 100)

    # the claw should be ready to grab now

    # return back to starting area


def get_left_tower(create):
    move_to_position(SPINDLE_MOTOR, 800, SIDE_TOWER_EXTEND_AMNT)
    create.forward_for(15, 100)
    msleep(100)
    create.turn_for(-7, 100)
    msleep(100)

    # the claw should be ready to grab now

    # return back to starting area now


def realign(create):
    create.wall_follow_till(distance=20, speed=100, condition_check=get_create_lfcliff_amt, condition=BLACK_THRESH)
    create.wall_follow_till(distance=20, speed=50, condition_check=get_create_rfcliff_amt, condition=BLACK_THRESH)
    msleep(100)
    create.turn_for(-45, 100)
    msleep(100)
    create.backward_for(10, 100)


def main():
    # connect create
    create_connect()
    print "Create connected"
    create_full()

    create = CreateLibrary()

    clear_motor_position_counter(SPINDLE_MOTOR)

    # botguy_status, mayor_status = get_tower_pos()
    # unknown_count = 0
    #
    # while botguy_status == "UNKNOWN" or mayor_status == "UNKNOWN":
    #     print "Can't detect one of the objects:"
    #     print "Botguy: " + botguy_status
    #     print "Mayor: " + mayor_status
    #     print "Retrying on iteration: " + str(unknown_count)
    #
    #     botguy_status, mayor_status = get_tower_pos()
    #
    #     if unknown_count == 5:
    #         # uh oh
    #         print "do some contingency stuff"
    #         break
    #
    #     unknown_count += 1
    #
    # print "Botguy: " + botguy_status
    # print "Mayor: " + mayor_status

    # positions have been grabbed by now, time to go get them

    #go forward and angle towards back corner
    # create.forward_for(2, 100)
    # msleep(100)
    # create.turn_for(35, 100)
    #
    # create.wall_follow_till(distance=20, speed=150, condition_check=create.get_both_bumpers, condition=1, forwards=True)
    #
    # # # turn and back up into corner
    # create.backward_for(2, 100)
    # msleep(100)
    # create.turn_for(-40, 100)
    # msleep(100)
    # create.backward_for(7, 100)
    # msleep(100)
    #
    # # turn to get it facing towards spawn box
    # create.forward_for(3, 100)
    # msleep(100)
    # create.turn_for(45, 100)
    #
    # create.wall_follow_till(distance=20, speed=150, condition_check=get_create_rfcliff_amt, condition=BLACK_THRESH, forwards=False)
    # create.backward_for(3, 100)
    # create.wall_follow_till(distance=20, speed=150, condition_check=get_create_rfcliff_amt, condition=BLACK_THRESH, forwards=False)

    create.forward_for(2, 100)
    msleep(100)
    create.turn_for(38, 100)
    msleep(100)
    realign(create)
    msleep(100)

    get_right_tower(create)
    realign(create)

    get_middle_tower(create)


    create_disconnect()



if __name__ == "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(), "w", 0)
    main()
