# ros_gridlocalization
A python program to make ros simulated robot localize in the given map using histogram/grid location

The starter code is available from https://github.com/DeepBlue14/uml_hmm. Under scripts there is a python code name "histogram.py" and "histogram1.py" which localizes the robot in the map given from left to right and vice versa respectively. The python code subcribes to "/robot/wall_door_sensor" topics to get the sensor reading of the robot and publishes the speed and rotation to the topic "/robot/cmd_vel". The ouput is an array which provides the bins/grids where the robot is localized

To run this simulation on one node(terminal) run "roslaunch ros_gridlocalization hmm.launch" which opens the racetrack and on another node run "rosrun ros_gridlocaliztion histogram.py" which makes the robot move and localizes its position.
