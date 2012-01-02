cmake_minimum_required(VERSION 2.8.0)
project(rospkg)
find_package(catkin)
catkin_project(rospkg
  PYTHONPATH src
  )
enable_python(rospkg)
