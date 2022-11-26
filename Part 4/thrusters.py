#!/usr/bin/env python
import rospy
from gazebo_msgs.srv import *


def apply_body_wrench_client(body_name, reference_frame, reference_point, wrench, start_time, duration):
    """
    Function to call /gazebo/apply_body_wrench' service
    """
    rospy.wait_for_service('/gazebo/apply_body_wrench')
    try:
        # create ServiceProxy object to call /gazebo/apply_body_wrench' service, passing ApplyBodyWrench 
        # as payload
        apply_body_wrench = rospy.ServiceProxy('/gazebo/apply_body_wrench', ApplyBodyWrench)
        # send service call with given parameters
        apply_body_wrench(body_name, reference_frame, reference_point, wrench, start_time, duration)
    except rospy.ServiceException as e:
        print("service call failure %s" % e)


def callback(data):
    """
    Callback function for listener, which publishes thruster commands using
    apply_body_wrench_client given respective data
    """
    rospy.loginfo(rospy.get_caller_id() + "Forces: %s", data.force)
    rospy.loginfo(rospy.get_caller_id() + "Torques: %s", data.torque)
    # define service call parameters according to obtained data
    duration = 1
    body_name = 'nessie::base_link'
    start_time = rospy.Time(secs=0, nsecs=0)
    duration = rospy.Duration(secs=duration, nsecs=0)
    reference_point = geometry_msgs.msg.Point(x=0, y=0, z=0)
    wrench = geometry_msgs.msg.Wrench(
        force=geometry_msgs.msg.Vector3(
            x=data.force.x,
            y=data.force.y,
            z=data.force.z),
        torque=geometry_msgs.msg.Vector3(
            x=data.torque.x,
            y=data.torque.y,
            z=data.torque.z))
    # call required service using apply_body_wrench_client
    apply_body_wrench_client(body_name, "", reference_point, wrench, start_time, duration)


def listener():
    """
    Set up a subsciber, which reads the data from /rexrov/thruster_manager/input
    topic, and issues respective thruster commands via callback function
    """
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/rexrov/thruster_manager/input", geometry_msgs.msg.Wrench, callback)
    # keep listener alive while program runs
    rospy.spin()


if __name__ == "__main__":
    # launch listener
    listener()