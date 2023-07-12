# AMR - FINAL PROJECT PRESENTATION : vr-183394

The objective is to move the turtlebot with unique algorithm to the maximum number of given goals ,avoiding the obstacles in the arena.

![Arena - Final Project](/final.png)


## ALGORITHM

The BUG 2 algorithm is used in the project and it is optimized to reach the goal given in the problem statement.

- The shortest path between the initial position of the Turtlebot and the goal is determined.
- Now, the robot turns to orient it’s front side towards the goal and moves towards the goal.
- Whenever an obstacle is detected in-front of the Turtlebot, it moves goes around the obstacle to join back in the shortest line analysed earlier.
- This way the Bug 2 algorithm proves to be more optimized than Bug 0 and faster than Bug 1 algorithm.

![Bug 2 Algorithm](/bug2.png)

The distance between the current location and the target is calculated using the formula,

![Euclidean Distance Formula](/eucl.png)

## SIDE PRIORITY

The main program (final_project.py) is designed with alternate of the left-side priority rule and right-side priority rule.

![Left Hand and Right Hand Priority](/lr.png)


## IMPLEMENTATION OF ALGORITHM

- The goal points are subscribed from the /goals topic and assigned to variables for global usage.

![Initial position and orientation of the Turtlebot.](/1.png)

- The robot orients itself and moves until the obstacle.

![Turtlebot orients towards the shortest path to the goal.](/2.png)

![Turtlebot encounters obstacle.](/3.png)

- Once, the obstacle is encountered, it goes around the obstacle and joins back in the original path.

![Turtlebot re-orients the he  (Left side priority) to go around the obstacle.](/4.png)

- The obstacle avoidance is implemented by follow_wall() function, which is implemented in both left-side priority rule and also right-side priority rule.

![Turtlebot moves around the obstacle.](/5.png)

- Once the robot joins back in the path, the should_leave_wall() function invokes the face_goal and orients the robot to move towards the goal.

![Turtlebot joins back in the shortest path to the goal.](/6.png)
![Turtlebot reaches the goal.](/7.png)

## RESULTS FROM PRACTICE-GOALS

- No. of goals reached = 3
- Total Rewards acquired = 600
