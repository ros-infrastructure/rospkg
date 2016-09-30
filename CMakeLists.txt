cmake_minimum_required(VERSION 2.8.0)
project(rospkg)
find_package(catkin REQUIRED)
catkin_package()
catkin_python_setup()

#install(FILES stack.yaml DESTINATION share/${PROJECT_NAME})

if(CATKIN_ENABLE_TESTING)
  catkin_add_nosetests(test)
endif()
