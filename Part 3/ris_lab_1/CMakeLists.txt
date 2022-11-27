cmake_minimum_required(VERSION 2.8.3)
project(ris_lab_1)

find_package(
    catkin REQUIRED COMPONENTS
        rospy
        nav_msgs
        geometry_msgs
        sensor_msgs
        topic_tools
)
catkin_package(
    CATKIN_DEPENDS
        rospy
        nav_msgs
        geometry_msgs
        sensor_msgs
        topic_tools
)
include_directories(${catkin_INCLUDE_DIRS})
catkin_install_python(
    PROGRAMS
        thruster_manager.py
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
