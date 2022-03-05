cmake_minimum_required(VERSION 2.8.3)
project(baxter_ras_interface)

find_package(catkin REQUIRED COMPONENTS
    actionlib
    baxter_core_msgs
    baxter_interface
    baxter_maintenance_msgs
    control_msgs
    cv_bridge
    geometry_msgs
    roscpp
    rospy
    sensor_msgs
    std_msgs
    trajectory_msgs
    message_generation
)

add_service_files(
    FILES
    Calibrado.srv
    Info.srv
    Cor.srv
    AutoInfo.srv
    Coordenadas.srv
    InfoCoor.srv
    Coordinates.srv
    infoz.srv
    infoxyz.srv
    juego_dificultad.srv
    auxiliar.srv
)
add_message_files(
  FILES
  Num.msg
)
generate_messages(DEPENDENCIES std_msgs)
catkin_package()

include_directories(
    ${catkin_INCLUD_LIBS}
)
