# Write a node similar to teleop_twist_keyboard that publishes forces
# and torques to control the AUV. Your node must publish to the
# topic/rexrov/thruster_manager/input

# Since teleop_twist_keyboard does not exist in the repository, we chose to
# use vehicle_keyboard_teleop.py as a sample solution to this task

# CHANGES

# instead of importing Twist, Accel, Vector3 we only import Wrench and Vector3
# we do not require Bool and numpy so we also remove those
# next we changed the topic we publish to, to /rexrov/thruster_manager/input
# finally, we changed the message type to Wrench, so the cmd.linear became cmd.force
# and cmd.angular became cmd.torque


#!/usr/bin/env python

from __future__ import print_function
import os
import time
import sys, select, termios, tty
import rospy
from geometry_msgs.msg import Wrench, Vector3

class KeyBoardVehicleTeleop:
    def __init__(self):
        # Class Variables
        self.settings = termios.tcgetattr(sys.stdin)

        # Speed setting
        self.speed = 2  # 1 = Slow, 2 = Fast
        self.t = Vector3(0, 0, 0)  # torque for Publish
        self.f = Vector3(0, 0, 0)  # force for publishing

        # User Interface
        self.msg = """
    Control Your Vehicle!
    ---------------------------
    Moving around:
        W/S: X-Axis (forward/backwards)
        A/D: Y-Axis (left/right)
        X/Z: Z-Axis (up/down)
        Q/E: Yaw
        I/K: Pitch
        J/L: Roll
    Slow / Fast: 1 / 2
    CTRL-C to quit
            """

        # Publish to /rexrov/thruster_manager/input topic
        self._output_pub = rospy.Publisher(
            '/rexrov/thruster_manager/input', Wrench, queue_size=10)
        # print our user instructions/interface message
        print(self.msg)

        # Ros Spin
        rate = rospy.Rate(500)  # 50hz
        while not rospy.is_shutdown():
            rate.sleep()
            self._parse_keyboard()

    # Every spin this function will return the key being pressed
    # Only works for one key per spin currently, thus limited control exploring alternative methods
    def _get_key(self):
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)

        return key

    def _parse_keyboard(self):
        # Save key peing pressed
        key_press = self._get_key()

        # Set Vehicle Speed #
        if key_press == "1":
            self.speed = 1
        if key_press == "2":
            self.speed = 2

        # use Wrench()
        cmd = Wrench()

        # If a key is pressed assign relevent linear / angular vel
        if key_press != '':
            # Applying the forces:
            # Forward
            if key_press == "w":
                self.f.x = self.speed
            # Backwards
            if key_press == "s":
                self.f.x = self.speed * -1  # negative direction
            # Left
            if key_press == "a":
                self.f.y = self.speed
            # Right
            if key_press == "d":
                self.f.y = self.speed * -1  # negative direction
            # Up
            if key_press == "x":
                self.f.z = self.speed
            # Down
            if key_press == "z":
                self.f.z = self.speed * -1  # negative direction

            # Applying the torque:
            # Roll Left
            if key_press == "j":
                self.t.x = self.speed
            # Roll Right
            if key_press == "l":
                self.t.x = self.speed * -1  # negative direction
            # Pitch Down
            if key_press == "i":
                self.t.y = self.speed
            # Pitch Up
            if key_press == "k":
                self.t.y = self.speed * -1  # negative direction
            # Yaw Left
            if key_press == "q":
                self.t.z = self.speed
            # Yaw Right
            if key_press == "e":
                self.t.z = self.speed * -1  # negative direction

        else:
            # If no button is pressed reset values to 0
            self.f = Vector3(0, 0, 0)
            self.t = Vector3(0, 0, 0)

        # Store velocity message into Twist format
        cmd.torque = self.t
        cmd.force = self.f

        # If ctrl+c kill node
        if (key_press == '\x03'):
            rospy.loginfo('Keyboard Interrupt Pressed')
            rospy.loginfo('Shutting down [%s] node' % node_name)

            # Set twists to 0
            cmd.torque = Vector3(0, 0, 0)
            cmd.force = Vector3(0, 0, 0)
            self._output_pub.publish(cmd)

            exit(-1)

        # Publish message
        self._output_pub.publish(cmd)


if __name__ == '__main__':

    # Wait for 5 seconds, so the instructions are the last thing to print in terminal
    time.sleep(5)
    # Start the node
    node_name = os.path.splitext(os.path.basename(__file__))[0]
    rospy.init_node(node_name)
    rospy.loginfo('Starting [%s] node' % node_name)

    teleop = KeyBoardVehicleTeleop()

    rospy.loginfo('Shutting down [%s] node' % node_name)
