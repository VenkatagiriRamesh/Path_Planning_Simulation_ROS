#!/usr/bin/env python

# AMR FINAL PROJECT - VENKATAGIRI RAMESH : vr-183394

import rospy
import math
from geometry_msgs.msg import Twist
from goal_publisher.msg import PointArray
from gazebo_msgs.msg import ModelStates
from sensor_msgs.msg import LaserScan
from location import Location, necessary_heading
from dist import Dist
import tf.transformations as transform
import sys
global x, y, z, reward

x = []
y = []
z = []
reward = []

current_location = Location()
current_dists = Dist()

delta =.05
WALL_PADDING =.30
STRAIGHT = 0
LEFT = 1
RIGHT = 2
MSG_STOP = 3

def init_subs():
    rospy.init_node('final_project', anonymous=True)
    rospy.Subscriber('/gazebo/model_states', ModelStates, location_callback)
    rospy.Subscriber('scan', LaserScan, sensor_callback)
    rospy.Subscriber('goals', PointArray,goals_callback)

def goals_callback(data):
    global x, y, reward
    for i in range(0,len(data.goals)):
        x.append(data.goals[i].x)
        y.append(data.goals[i].y)
        z.append(data.goals[i].z)
        reward.append(data.goals[i].reward)

def location_callback(data):
    p = data.pose[1].position
    q = (
            data.pose[1].orientation.x,
            data.pose[1].orientation.y,
            data.pose[1].orientation.z,
            data.pose[1].orientation.w)
    t = transform.euler_from_quaternion(q)[2]
    current_location.update_location(p.x, p.y, t)

def sensor_callback(data):
    current_dists.update(data)

class Goal:

    def __init__(self,a,b,c):
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        self.x1 = a
        self.y1 = b
        self.z1 = c
        self.lh = None
        self.encountered_wall_at = (None, None)

    def go(self, direction):
        cmd = Twist()
        if direction == STRAIGHT:
            cmd.linear.x = 0.29
        elif direction == LEFT:
            cmd.angular.z = 0.25
        elif direction == RIGHT:
            cmd.angular.z = -0.25
        elif direction == MSG_STOP:
            cmd.linear.x = 0
            cmd.angular.z = 0
        self.pub.publish(cmd)

    def go_until_obstacle(self):
        print "Moving towards the goal"
        while current_location.distance(self.x1, self.y1) > delta:
            (frontdist, _, _) = current_dists.get()
            if frontdist <= WALL_PADDING:
                return True

            if current_location.facing_point(self.x1, self.y1):
                self.go(STRAIGHT)
            elif current_location.faster_left(self.x1, self.y1):
                self.go(LEFT)
            else:
                self.go(RIGHT)
            rospy.sleep(.01)
        return False

    def follow_wall_left(self):
        print "Align and follow wall"
        while not self.should_leave_wall():
            (front, left, right) = current_dists.get()
            if front <= WALL_PADDING:
                self.go(LEFT)
            elif WALL_PADDING - .1 <= right <= WALL_PADDING + .05:
                self.go(STRAIGHT)
            elif right > WALL_PADDING + .05:
                self.go(RIGHT)
            elif left < 1 and right < 1:
                self.go(STRAIGHT)
            else:
                self.go(LEFT)
            rospy.sleep(.01)

    def follow_wall_right(self):
        print "Align and Follow wall"
        while current_dists.get()[0] <= WALL_PADDING:
            self.go(RIGHT)
            rospy.sleep(.01)
        while not self.should_leave_wall():
            (front, left, right) = current_dists.get()
            if front <= WALL_PADDING:
                self.go(RIGHT)
            elif WALL_PADDING - .17 <= left <= WALL_PADDING + .1:
                self.go(STRAIGHT)
            elif left > WALL_PADDING + .1:
                self.go(LEFT)
            elif left < 1 and right < 1:
                self.go(STRAIGHT)
            else:
                self.go(RIGHT)
            rospy.sleep(.01)

    def should_leave_wall(self):
        (x, y, _) = current_location.current_location()
        if None in self.encountered_wall_at:
            self.encountered_wall_at = (x, y)
            self.lh = necessary_heading(x, y, self.x1, self.y1)
            return False
        t_angle = necessary_heading(x, y, self.x1, self.y1)
        (ox, oy) = self.encountered_wall_at
        od = math.sqrt((ox-self.x1)**2 + (oy-self.y1)**2)
        cd = math.sqrt( (x-self.x1)**2 +  (y-self.y1)**2)
        dt = 0.01
        if self.lh - dt <= t_angle <= self.lh + dt and not near(x, y, ox, oy):
            if cd < od:
                print "End of wall"
                return True
        return False

    def face_goal(self):
        while not current_location.facing_point(self.x1, self.y1):
            if current_location.faster_left(self.x1, self.y1):
                self.go(LEFT)
            else:
                self.go(RIGHT)
            rospy.sleep(.01)

def near(cx, cy, x, y):
    nearx = x - .2 <= cx <= x + .2
    neary = y - .2 <= cy <= y + .2
    return nearx and neary


if __name__ == '__main__':
    init_subs()
    print ("AMR Final Project - VENKATAGIRI RAMESH : vr-183394")
    rospy.sleep(5)
    reward_sum = 0
    flag = 0
    for j in range(0,len(x)):
        print "Current Target Goal : ", (x[j],y[j])
        goal = Goal(x[j],y[j],z[j])
        while current_location.distance(x[j], y[j]) > delta:
            hit_wall = goal.go_until_obstacle()
            if hit_wall:
                if flag == 0 :
                    goal.follow_wall_left()
                    flag = 1
                else:
                    goal.follow_wall_right()
                    flag = 0
            goal.face_goal()
        goal.go(MSG_STOP)
        print "Reached Target Goal : ", (x[j], y[j])
        reward_sum = reward_sum + reward[j]
        print "Total Reward :", (reward_sum)
        rospy.sleep(1)
    rospy.is_shutdown()
