#! /usr/bin/bash

# install ROS
# from https://wiki.ros.org/melodic/Installation/Ubuntu
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116
sudo apt update
sudo apt install ros-melodic-ros-base
sudo rosdep init
rosdep update

# install sphero_ros
# from https://github.com/mmwise/sphero_ros
source /opt/ros/melodic/setup.sh
mkdir -p sphero_ros/src
cd sphero_ros/src
git clone https://github.com/mmwise/sphero_ros.git
cd ..
catkin_make
catkin_make install
cd ..

# install python dependencies
python2 -m pip install -U pytest
