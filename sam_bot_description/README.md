# Pour la partie Navigation
- Utiliser le package rqt_robot_steering faire en sorte que le pakage envoie les commandes sur le bon topic. Le Robot doit se déplacer dasn Gazebo et RVIZ
- Faire son propre noeud qui utilise le retour du lidar

- Dans l'urdf, pour l'odométrie : dans les paramètres du plugin diff_drive_controller.so mettre publish_odom_tf à true
(et ne plus lancer le noeuds ekf)

Pour gérer les coefficient de frottements:
```xml
<gazebo link=[votre roue]>
  <mu1>1.2</mu1>
  <mu2>1.2</mu2>
  <kp>500000.0</kp>
  <kd>10.0</kd>
  <minDepth>0.001</minDepth>
  <maxVel>0.1</maxVel>
  <material>Gazebo/FlatBlack</material>
</gazebo>
```
# Nav2 URDF Setup Tutorial - Differential Drive Robot

Tutorial code referenced in https://navigation.ros.org/setup_guides/urdf/setup_urdf.html

This package implements a URDF description for a simple differential drive robot. It includes the complete urdf files, launch files, build files and rviz configuration to replicate the tutorial in the link above

```bash
# Map and Costmap
ros2 launch slam_toolbox online_async_launch.py
ros2 launch nav2_bringup navigation_launch.py
ros2 run nav2_costmap_2d nav2_costmap_2d_markers voxel_grid:=/local_costmap/voxel_grid visualization_marker:=/my_marker

```

```bash
# Footprint
ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 map odom
ros2 launch nav2_bringup navigation_launch.py params_file:=/home/nathan/ros2_ws/src/navigation2_tutorials/sam_bot_description/config/nav2_params.yaml
# for foxy : https://github.com/ros-planning/navigation2/blob/foxy-devel/nav2_bringup/bringup/params/nav2_params.yaml#L61-L82
# In RVIZ : set frame to map to see footprint
```
