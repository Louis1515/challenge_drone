import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Empty
from sensor_msgs.msg import Image
import cv2
import time
import numpy as np

from sensor_msgs.msg import CompressedImage
from sensor_msgs.msg import Range
from geometry_msgs.msg import Pose

import threading


class Drone():
    command_attempts = 3

    def __init__(self, i):
        self.name = "drone" + str(i)

        rospy.init_node("robot_control_node", anonymous=True)

        """Initialise publisher"""
        self.vel_publisher = rospy.Publisher("/drone%s/cmd_vel"%i, Twist, queue_size=1)
        self.takeoff_publisher = rospy.Publisher("/drone%s/takeoff"%i, Empty, queue_size=1)
        self.land_publisher = rospy.Publisher("/drone%s/land"%i, Empty, queue_size=1)
        self.reset_publisher = rospy.Publisher("/drone%s/reset"%i, Empty, queue_size=1)
        
        """Initialise subscriber"""
        rospy.Subscriber("/drone%s/gt_pose" % i, Pose, self.__read_pos)
        rospy.Subscriber("/drone%s/gt_vel"%i,Twist, self.__read_vel)
        rospy.Subscriber("/drone%s/sonar"%i, Range, self.__read_sonar)
        self.subscriber = rospy.Subscriber("/drone%s/front_camera/image_raw/compressed"%i,
                                            CompressedImage, self.__camera_callback,  queue_size = 1)
        
        self.cmd = Twist()
        self.cmd.linear.x = 0
        self.cmd.linear.y = 0
        self.cmd.linear.z = 0
        self.cmd.angular.x = 0
        self.cmd.angular.y = 0
        self.cmd.angular.z = 0
        self.linearV_max = 100
        self.angularV_max = 100

        self.position = [0, 0, 0]
        self.orientation = [0, 0, 0, 0]
        self.vel = Twist()
        self.sonar = 0

        self.is_flying = False
        self.is_on = True
        #image subscriber
        self.view = np.zeros((360,640,3))

    def __camera_callback(self, ros_data):
        np_arr = np.fromstring(ros_data.data, np.uint8)
        self.view = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    def __read_pos(self, data):
        self.pose = data
        self.position = [getattr(self.pose.position, c) for c in "xyz"]
        self.orientation = [getattr(self.pose.orientation, c) for c in "xyzw"]

    def __read_vel(self, data):
        self.vel = data

    def __read_sonar(self, data):
        self.sonar = data.range

    def turn_off(self):
        self.is_on = False
        self.stop()
        self.land()
        self.cmd_thread.join()

    def turn_on(self):
        self.cmd_thread = threading.Thread(target=self.cmd_vel_thread)
        self.cmd_thread.start()

    def cmd_vel_thread(self):
        while self.is_on:
            if self.is_flying : 
                connections = self.vel_publisher.get_num_connections()
                if connections > 0:
                    self.vel_publisher.publish(self.cmd)
                else:
                    print("%s fail to publish %s/cmd_vel"%(self.name,self.name))
            time.sleep(0.1)
                
    def get_vel(self):
        return self.vel

    def stop(self):
        #set velocity to zero
        self.set_linear_velocity([0, 0, 0])
        self.set_angular_velocity([0, 0, 0])

    def take_off(self):
        """
        This is because publishing in topics sometimes fails the first time you publish.
        In continuous publishing systems, this is no big deal, but in systems that publish only
        once, it IS very important.
        """
        connections = self.takeoff_publisher.get_num_connections()
        if connections > 0:
            for i in range(self.command_attempts):
                self.takeoff_publisher.publish(Empty())
            self.is_flying = True
            print("%s takeoff cmd published" % self.name)
        else:
            print("%s fail connect to %s/take_off"%(self.name,self.name))
                
    def land(self):
        """
        This is because publishing in topics sometimes fails the first time you publish.
        In continuous publishing systems, this is no big deal, but in systems that publish only
        once, it IS very important.
        """
        connections = self.land_publisher.get_num_connections()
        if connections > 0:
            for i in range(self.command_attempts):
                self.land_publisher.publish(Empty())
            print("%s land cmd published"%self.name)
            self.is_flying=False
        else:
            print("%s fail to connect to %s/land"%(self.name, self.name))

    def set_linear_velocity(self, v):
        self.cmd.linear.x = v[0]
        self.cmd.linear.y = v[1]
        self.cmd.linear.z = v[2]

    def set_angular_velocity(self, v):
        self.cmd.angular.x = v[0]
        self.cmd.angular.y = v[1]
        self.cmd.angular.z = v[2]


    def up(self, speed):
        """Up tells the drone to ascend. Pass in an int from 0-100."""
        print('up(val=%d)' % speed)
        self.cmd.linear.z = self.linearV_max * speed / 100

    def down(self, speed):
        """Down tells the drone to descend. Pass in an int from 0-100."""
        print('down(val=%d)' % speed)
        self.cmd.linear.z = - self.linearV_max * speed / 100

    def forward(self, speed):
        """Forward tells the drone to go forward. Pass in an int from 0-100."""
        print('forward(val=%d)' % speed)
        self.cmd.linear.x = self.linearV_max * speed / 100

    def backward(self, speed):
        """Backward tells the drone to go in reverse. Pass in an int from 0-100."""
        print('backward(val=%d)' % speed)
        self.cmd.linear.x = - self.linearV_max * speed / 100

    def right(self, speed):
        """Right tells the drone to go right. Pass in an int from 0-100."""
        print('right(val=%d)' % speed)
        self.cmd.linear.y = self.linearV_max * speed / 100

    def left(self, speed):
        """Left tells the drone to go left. Pass in an int from 0-100."""
        print('left(val=%d)' % speed)
        self.cmd.linear.y = - self.linearV_max * speed / 100

    def clockwise(self, speed):
        """
        Clockwise tells the drone to rotate in a clockwise direction.
        Pass in an int from 0-100.
        """
        print('clockwise(val=%d)' % speed)
        self.cmd.angular.z = self.angularV_max * speed / 100

    def counter_clockwise(self, speed):
        """
        CounterClockwise tells the drone to rotate in a counter-clockwise direction.
        Pass in an int from 0-100.
        """
        print('counter_clockwise(val=%d)' % speed)
        self.cmd.angular.z = - self.angularV_max * speed / 100