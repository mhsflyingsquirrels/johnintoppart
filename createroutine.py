#!/usr/bin/python
import os
import sys
from wallaby import *

KP = 5
SPINDLE_MOTOR = 0
SIDE_TOWER_BOTGUY_EXTEND_AMNT = 5186
SIDE_TOWER_MAYOR_EXTEND_AMNT = 4600
MIDDLE_TOWER_BOTGUY_EXTEND_AMNT = 9275
MIDDLE_TOWER_MAYOR_EXTEND_AMNT = 8500
DROP_EXTEND_AMNT = 2000

CLAW_OPEN = 0
CLAW_CLOSE = 1053
CLAW_PORT = 0

BLACK_THRESH = 2000
GREY_THRESH = 2800

TPHAT_PORT = 0

MOVEMENT_DEBUG = True

SPEED_COMPENSATION = 0


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

    def lcliff_not_front_line_follow(self, distance, speed, thresh):
        set_create_distance(0)

        while -get_create_distance() < distance:
            if get_create_lcliff_amt() < thresh:
                create_drive_direct(speed / 2, speed)
            elif get_create_lcliff_amt() > thresh:
                create_drive_direct(speed, speed / 2)

        create_stop()

    # bad programming
    def rcliff_not_front_line_follow(self, distance, speed, thresh):
        set_create_distance(0)

        while -get_create_distance() < distance:
            if get_create_rcliff_amt() < thresh:
                create_drive_direct(speed, speed / 2)
            elif get_create_rcliff_amt() > thresh:
                create_drive_direct(speed / 2, speed)

    def rcliff_line_follow_special(self, speed, thresh):
        while analog(TPHAT_PORT) < thresh:
            if get_create_rcliff_amt() < thresh:
                create_drive_direct(speed, speed * 2)
            elif get_create_rcliff_amt() > thresh:
                create_drive_direct(speed * 2, speed)

        create_stop()

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
        if both is False:
            while get_create_lbump() == 0 and get_create_rbump() == 0:
                msleep(5)

        else:
            while get_create_lbump() != 1 or get_create_rbump() != 1:
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

    def drive_till(self, speed, condition_check, condition, forwards=True):
        status = "None"
        while condition_check() == 0 or condition_check() > condition:
            if forwards:
                create_drive_direct(speed, speed)
            else:
                create_drive_direct(-speed, -speed)

            self.smart_print(string="Condition: ", value=condition_check())

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

def get_right_tower(create, retrieve_object):
    if retrieve_object == "BOTGUY":
        SIDE_TOWER_EXTEND_AMNT = SIDE_TOWER_BOTGUY_EXTEND_AMNT
    else:
        SIDE_TOWER_EXTEND_AMNT = SIDE_TOWER_MAYOR_EXTEND_AMNT

    move_to_position(SPINDLE_MOTOR, 800, SIDE_TOWER_EXTEND_AMNT)
    msleep(100)
    if get_motor_done(SPINDLE_MOTOR):
        move_to_position(SPINDLE_MOTOR, 800, SIDE_TOWER_EXTEND_AMNT)
        print "Motor Done Pos: " + str(get_motor_position_counter(SPINDLE_MOTOR))

    create.drive_till(speed=100, condition_check=get_create_lcliff_amt, condition=BLACK_THRESH, forwards=True)
    create.forward_for(5, 100)
    create.drive_till(speed=100, condition_check=get_create_lcliff_amt, condition=BLACK_THRESH, forwards=True)

    create.turn_for(5, 100)
    msleep(100)
    create.forward_for(17, 100)
    msleep(100)

    # the claw should be ready to grab now
    set_servo_position(CLAW_PORT, CLAW_CLOSE)
    msleep(100)
    move_to_position(SPINDLE_MOTOR, 800, DROP_EXTEND_AMNT)
    msleep(100)
    if get_motor_done(SPINDLE_MOTOR):
        move_to_position(SPINDLE_MOTOR, 800, DROP_EXTEND_AMNT)
        print "Motor Done Pos: " + str(get_motor_position_counter(SPINDLE_MOTOR))


    msleep(3000)

    # return back to starting area
    create.backward_for(5, 100)
    msleep(100)
    create.turn_for(-68, 100)
    msleep(100)
    create.forward_for(30, 100)
    msleep(100)

    # create.turn_for(10, 100)
    set_servo_position(CLAW_PORT, CLAW_OPEN)
    msleep(100)

    # being realignment process
    create.backward_for(42, 200)
    msleep(100)
    create.turn_for(20, 100)
    msleep(100)
    create.backward_for(28, 200)
    msleep(100)
    create.turn_for(35, 100)

    # create.turn_for(-25, 100)
    # msleep(1000)
    # create.forward_for(3, 100)
    # msleep(1000)
    # create.turn_for(-35, 100)

    # create.forward_until_bumper(100, both=False)
    # msleep(100)
    # create.backward_for(2, 100)
    # msleep(100)
    # create.turn_for(-45, 100)


def get_middle_tower(create, retrieve_object):
    if retrieve_object == "BOTGUY":
        MIDDLE_TOWER_EXTEND_AMNT = MIDDLE_TOWER_BOTGUY_EXTEND_AMNT
    else:
        MIDDLE_TOWER_EXTEND_AMNT = MIDDLE_TOWER_MAYOR_EXTEND_AMNT

    move_to_position(SPINDLE_MOTOR, 800, MIDDLE_TOWER_EXTEND_AMNT)
    msleep(100)
    if get_motor_done(SPINDLE_MOTOR):
        move_to_position(SPINDLE_MOTOR, 800, MIDDLE_TOWER_EXTEND_AMNT)
        print "Motor Done Pos: " + str(get_motor_position_counter(SPINDLE_MOTOR))


    create.forward_for(5, 100)
    msleep(100)
    create.turn_for(-40, 100)
    create.forward_for(12, 100)
    msleep(100)

    create.turn_for(40, 100)
    create.backward_for(10, 100)

    create.drive_till(speed=100, condition_check=get_create_lfcliff_amt, condition=BLACK_THRESH, forwards=True)
    create.forward_for(5, 100)
    create.drive_till(speed=100, condition_check=get_create_lfcliff_amt, condition=BLACK_THRESH, forwards=True)
    msleep(100)

    create.forward_for(12, 100)
    msleep(100)


    # the claw should be ready to grab now
    set_servo_position(CLAW_PORT, CLAW_CLOSE)
    msleep(100)
    move_to_position(SPINDLE_MOTOR, 800, DROP_EXTEND_AMNT)
    msleep(100)
    if get_motor_done(SPINDLE_MOTOR):
        move_to_position(SPINDLE_MOTOR, 800, DROP_EXTEND_AMNT)
        print "Motor Done Pos: " + str(get_motor_position_counter(SPINDLE_MOTOR))
    msleep(5000)

    # return back to starting area
    create.backward_for(37, 100)
    msleep(100)
    create.turn_for(-40, 100)
    msleep(100)
    set_servo_position(CLAW_PORT, CLAW_OPEN)
    msleep(100)

    # begin realignent process
    # create.turn_for(40, 100)
    # create.forward_for(2, 100)
    # create.turn_for(35, 100)



def get_left_tower(create, retrieve_object):
    if retrieve_object == "BOTGUY":
        SIDE_TOWER_EXTEND_AMNT = SIDE_TOWER_BOTGUY_EXTEND_AMNT
    else:
        SIDE_TOWER_EXTEND_AMNT = SIDE_TOWER_BOTGUY_EXTEND_AMNT

    move_to_position(SPINDLE_MOTOR, 800, SIDE_TOWER_EXTEND_AMNT)
    msleep(100)
    if get_motor_done(SPINDLE_MOTOR):
        move_to_position(SPINDLE_MOTOR, 800, SIDE_TOWER_EXTEND_AMNT)
        print "Motor Done Pos: " + str(get_motor_position_counter(SPINDLE_MOTOR))


    create.drive_till(speed=100, condition_check=get_create_lcliff_amt, condition=BLACK_THRESH, forwards=True)
    create.forward_for(5, 100)
    create.drive_till(speed=100, condition_check=get_create_lfcliff_amt, condition=GREY_THRESH, forwards=True)

    create.turn_for(-45, 100)
    create.rcliff_line_follow_special(speed=75, thresh=GREY_THRESH)
    msleep(10)

    # go up to the left tower
    create.turn_for(39, 100)
    msleep(100)
    create.forward_for(25, 100)

    # the claw should be ready to grab now
    set_servo_position(CLAW_PORT, CLAW_CLOSE)
    msleep(100)
    move_to_position(SPINDLE_MOTOR, 800, DROP_EXTEND_AMNT)
    msleep(100)
    if get_motor_done(SPINDLE_MOTOR):
        move_to_position(SPINDLE_MOTOR, 800, DROP_EXTEND_AMNT)
        print "Motor Done Pos: " + str(get_motor_position_counter(SPINDLE_MOTOR))
    msleep(3000)

    create.backward_for(3, 100)

    # return back to starting area now
    create.turn_for(-85, 100)
    msleep(100)
    create.forward_for(25, 100)
    msleep(100)
    set_servo_position(CLAW_PORT, CLAW_OPEN)
    msleep(100)
    create.backward_for(20, 200)
    msleep(100)
    create.turn_for(40, 100)
    create.backward_for(100, 200)
    msleep(100)
    create.turn_for(40, 100)

    #
    # msleep(2000)
    #
    # create.forward_for(10, 100)
    #
    # create.turn_for(-30, 100)
    # # begin realignment process
    # speed = 75
    #
    # while get_create_lfcliff_amt() > BLACK_THRESH and get_create_rfcliff_amt() > BLACK_THRESH:
    #     if analog(TPHAT_PORT) < BLACK_THRESH:
    #         create_drive_direct(speed, speed * 2)
    #     elif analog(TPHAT_PORT) > BLACK_THRESH:
    #         create_drive_direct(speed * 2, speed)
    #
    # i = 0
    #
    # while i < 35:
    #     if analog(TPHAT_PORT) < BLACK_THRESH:
    #         create_drive_direct(speed, speed * 2)
    #     elif analog(TPHAT_PORT) > BLACK_THRESH:
    #         create_drive_direct(speed * 2, speed)
    #
    #     i += 1
    #
    #
    # # create.wall_follow_till(distance=20, speed=100, condition_check=get_create_lfcliff_amt, condition=BLACK_THRESH)
    # # create.wall_follow_till(distance=20, speed=50, condition_check=get_create_rfcliff_amt, condition=BLACK_THRESH)
    # msleep(100)
    # create.turn_for(-45, 100)
    # msleep(100)
    # create.backward_for(10, 100)


    # create.turn_for(-30, 100)
    # msleep(100)
    # create.forward_for(20, 100)
    # msleep(100)
    # create.turn_for(20, 100)
    # create.forward_until_bumper(100, both=False)
    # msleep(100)
    # create.backward_for(2, 100)
    # msleep(100)
    # create.turn_for(-40, 100)


def realign_after_first(create):
    create.backward_for(90, 170)
    msleep(100)
    create.forward_for(5, 100)
    msleep(100)
    create.turn_for(-39, 100)
    msleep(100)
    create.drive_till(speed=100, condition_check=get_create_lfcliff_amt, condition=BLACK_THRESH, forwards=True)
    msleep(100)
    create.forward_for(15, 100)
    msleep(100)
    create.turn_for(39, 100)
    msleep(100)
    create.backward_for(15, 100)


def realign(create):
    # if get_create_wall_amt() < 16:
    #     while get_create_wall_amt() < 16:
    #         create_spin_CW(50)
    #         print get_create_wall_amt()
    #
    # create_stop()

    speed = 75

    while get_create_lfcliff_amt() > BLACK_THRESH and get_create_rfcliff_amt() > BLACK_THRESH:
        if analog(TPHAT_PORT) < BLACK_THRESH:
            create_drive_direct(speed, speed * 2)
        elif analog(TPHAT_PORT) > BLACK_THRESH:
            create_drive_direct(speed * 2, speed)

    i = 0

    while i < 35:
        if analog(TPHAT_PORT) < BLACK_THRESH:
            create_drive_direct(speed, speed * 2)
        elif analog(TPHAT_PORT) > BLACK_THRESH:
            create_drive_direct(speed * 2, speed)

        i += 1

    create_stop()

    # create.wall_follow_till(distance=20, speed=100, condition_check=get_create_lfcliff_amt, condition=BLACK_THRESH)
    # create.wall_follow_till(distance=20, speed=50, condition_check=get_create_rfcliff_amt, condition=BLACK_THRESH)
    msleep(100)
    create.turn_for(-45, 100)
    msleep(100)
    create.backward_for(10, 100)


def main():

    wait_for_light(1)

    # connect create
    create_connect()
    print "Create connected"
    create_full()

    create = CreateLibrary()

    clear_motor_position_counter(SPINDLE_MOTOR)
    print "CLeared motor"

    shut_down_in(120)

    msleep(100)

    enable_servo(CLAW_PORT)
    set_servo_position(CLAW_PORT, CLAW_OPEN)

    move_to_position(SPINDLE_MOTOR, 800, 100)

    botguy_status, mayor_status = get_tower_pos()
    unknown_count = 0

    while botguy_status == "UNKNOWN" or mayor_status == "UNKNOWN":
        print "Can't detect one of the objects:"
        print "Botguy: " + botguy_status
        print "Mayor: " + mayor_status
        print "Retrying on iteration: " + str(unknown_count)

        botguy_status, mayor_status = get_tower_pos()

        if unknown_count == 5:
            # uh oh
            print "do some contingency stuff"
            break

        unknown_count += 1

    print "Botguy: " + botguy_status
    print "Mayor: " + mayor_status

    towers_to_get = {"MAYOR": mayor_status, "BOTGUY": botguy_status}

    # positions have been grabbed by now, time to go get them
    create.forward_for(3, 100)
    create.turn_for(40, 100)
    msleep(100)

    # create_drive_direct(200, 150)
    # msleep(1000)
    # create_stop()

    # msleep(100)
    # create.turn_for(70, 100)
    # msleep(100)
    realign(create)
    msleep(100)

    if mayor_status == "RIGHT":
        print "going for mayor on right"
        get_right_tower(create, "MAYOR")
        towers_to_get.pop("MAYOR")

    elif mayor_status == "LEFT":
        print "going for mayor on left"
        get_left_tower(create, "MAYOR")
        towers_to_get.pop("MAYOR")

    else:
        if botguy_status == "LEFT":
            print "getting botguy on the left"
            get_left_tower(create, "BOTGUY")

        elif botguy_status == "RIGHT":
            print "getting botguy on right"
            get_right_tower(create, "BOTGUY")

        towers_to_get.pop("BOTGUY")

    # realign after dropping off first object
    realign_after_first(create)

    remaining_tower = towers_to_get[towers_to_get.keys()[0]]

    if remaining_tower == "RIGHT":
        get_right_tower(create, remaining_tower)
    elif remaining_tower == "LEFT":
        get_left_tower(create, remaining_tower)
    elif remaining_tower == "MID":
        get_middle_tower(create, remaining_tower)



    create_disconnect()



if __name__ == "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(), "w", 0)
    main()
