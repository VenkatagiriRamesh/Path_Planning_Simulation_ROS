# Path Planning Algorithm with ROS and Python

The objective is to move the turtlebot with unique algorithm to the maximum number of given goals ,avoiding the obstacles in the arena.

## Getting Started.

1. Launch Gazebo - Empty world with Turtlebot using the command

2. Load the arena by using the command (make sure, you have the arena model in appropriate directory)"

3. Launch the ROS package for the project using the command, roslaunch vr_183394_prj start.launch.

## Pre-requisites

1. Linux OS
2. ROS Kinetic
3. Gazebo
4. Goal list
5. Arena Model (from project issue in Gitlab)

## General Description

The ultimate goal of the project is to implement a optimize algorithm for the given scenario and reach the maximum number of goals in the arena.

![Arena - Final Project](/final.png)

## Topics and Services

**/goals** - This topic subscribes to the target goals.

**/scan** -  This topic subscribes to Laser scan data.

**/gazebo/model_states** - This subscribes to the current orientation and position of the robot.

**/cmd_vel** - This topic published the linear and angular velocity of the robot at each instance.

## Algorithm

The BUG 2 algorithm is used in the project and it is optimized to reach the goal given in the problem statement.

The shortest path between the initial position of the Turtlebot and the goal is determined. Now, the robot turns to orient it’s front side towards the goal and moves towards the goal. Whenever an obstacle is detected in-front of the Turtlebot, it moves goes around the obstacle to join back in the shortest line analysed earlier. This way the Bug 2 algorithm proves to be more optimized than Bug 0 and faster than Bug 1 algorithm.

![Bug 2 Algorithm](/bug2.png)

## Implementation of Algorithm

The goal points are subscribed from the /goals topic and assigned to variables for global usage.

The robot orients itself and moves until the obstacle. Once, the obstacle is encountered, it goes around the obstacle and joins back in the original path.

The obstacle avoidance is implemented by follow_wall() function, which is implemented in both left-side priority rule and also right-side priority rule.

Once the robot joins back in the path, the should_leave_wall() function invokes the face_goal and orients the robot to move towards the goal.

## Problem

The usage of either of left-side priority rule or right-side priority rule alone restricts the freedom of the robot to take decisions in a versatile way for each goal. This leads to greater amount of time taken by the robot to reach certain goals given.

## Solution

The main program (final_project.py) is designed with alternate of the left-side priority rule and right-side priority rule. Hence, for each of the given goal, in an alternate way the left hand priority rule and the right hand priority rule is used.
