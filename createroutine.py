#!/usr/bin/python
import os
import sys
from wallaby import *

KP = 5

# was 1000
BLACK_THRESH = 1500
print_value = None

MOVEMENT_DEBUG = True


# function to print values to console without repeating values


def smart_print(string, value):
    global print_value
    if print_value != value and MOVEMENT_DEBUG is True:
        print string + str(value)

    print_value = value


def cliff_line_follow(distance, speed):
    set_create_distance(0)

    while -get_create_distance() < distance:
        if get_create_lfcliff_amt() < BLACK_THRESH:
            create_drive_direct(speed, speed / 2)
        elif get_create_lfcliff_amt() > BLACK_THRESH:
            create_drive_direct(speed / 2, speed)

        smart_print("Distance: ", get_create_distance())

    create_stop()

# bad programming


def rcliff_not_front_line_follow(distance, speed):
    set_create_distance(0)

    while -get_create_distance() < distance:
        if get_create_rcliff_amt() < BLACK_THRESH:
            create_drive_direct(speed, speed / 2)
        elif get_create_rcliff_amt() > BLACK_THRESH:
            create_drive_direct(speed / 2, speed)

        smart_print("Distance: ", get_create_distance())


def drive_arc(speed, radius, distance):
    create_drive(speed, radius)

    while -get_create_distance() < distance:
        smart_print("Arc Distance: ", get_create_distance())

    create_stop()


# go backward for certain distance + speed


def backward_for(distance, speed):
    set_create_distance(0)
    create_drive_straight(-speed)

    while get_create_distance() < distance:
        smart_print("Distance: ", get_create_distance())

    create_stop()

# go forward for certain distance + speed (Forward = bumper)


def forward_for(distance, speed):
    set_create_distance(0)
    create_drive_straight(speed)

    while -get_create_distance() < distance:
        smart_print("Distance: ", get_create_distance())

    create_stop()

# only works on the right wall


def wall_follow(distanceFromWall, speed):
    error = get_create_wall_amt() - distanceFromWall
    smart_print("Error: ", error)

    turnRadius = error * KP

    if get_create_wall_amt() != distanceFromWall:
        create_drive(speed, turnRadius)
    else:
        backward_for(2, speed)

# positive is clockwise


def turn_for(angle, speed):
    set_create_normalized_angle(0)

    if angle > 0:  # clockwise
        print "spinning clockwise"
        create_spin_CW(speed)

        while get_create_normalized_angle() > -angle:
            smart_print("Angle: ", get_create_normalized_angle())

    elif angle < 0:
        print "spinnng counter clockwise"
        create_spin_CCW(speed)

        while -get_create_normalized_angle() > angle:
            smart_print("Angle: ", get_create_normalized_angle())

    create_stop()


def turn_motor_to_tick(motor, incr, tick):

    print "IM TURNING THE MOTOR RIGHT NOW"
    mrp(motor, incr, tick)
    msleep(100)

    # dumb
    block_motor_done(motor)


def forward_until_bumper(speed, both=True):
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


def gradual_servo(servo, pos, speed):
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


def twist_and_shout(ticks):
    for x in range(0, ticks):
        set_servo_position(FORKLIFT, 693)
        print "up"
        msleep(500)
        set_servo_position(FORKLIFT, 48)
        msleep(500)
        print "down"


def bad_motor(port, time, power):
    motor(port, power)
    msleep(time)
    ao()


def main():
    # connect create
    create_connect()
    print "Create connected"

    # start of program goes here


if __name__ == "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(), "w", 0)
    main()
