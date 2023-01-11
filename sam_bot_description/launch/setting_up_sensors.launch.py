import launch
from launch.substitutions import Command, LaunchConfiguration
from launch.actions import (DeclareLaunchArgument, GroupAction,
                            IncludeLaunchDescription, SetEnvironmentVariable)   
from launch import LaunchDescription
from launch.actions import TimerAction

import os
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    slam_toolbox_pkg_share = get_package_share_directory('slam_toolbox')
    nav2_bringup_pkg_share = get_package_share_directory('nav2_bringup')


    stdout_linebuf_envvar = SetEnvironmentVariable(
        'RCUTILS_LOGGING_BUFFERED_STREAM', '1')

    namespace = LaunchConfiguration('namespace')
    use_sim_time = LaunchConfiguration('use_sim_time')
    autostart = LaunchConfiguration('autostart')
    use_respawn = LaunchConfiguration('use_respawn')

    declare_namespace_cmd = DeclareLaunchArgument(
        'namespace',
        default_value='',
        description='Top-level namespace')
    
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true')
    
    declare_use_respawn_cmd = DeclareLaunchArgument(
        'use_respawn', default_value='False',
        description='Whether to respawn if a node crashes. Applied when composition is disabled.')
    
    declare_autostart_cmd = DeclareLaunchArgument(
        'autostart', default_value='true',
        description='Automatically startup the nav2 stack')
    
    nodes_group = GroupAction([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(slam_toolbox_pkg_share, 'launch/online_async_launch.py')),
            launch_arguments={'namespace': namespace,
                                'use_sim_time': use_sim_time,
                                'autostart': autostart,
                                'use_respawn': use_respawn}.items()),

            TimerAction(period=5.0,
                actions=[ IncludeLaunchDescription(
                    PythonLaunchDescriptionSource(os.path.join(nav2_bringup_pkg_share, 'launch/navigation_launch.py')),
                    launch_arguments={'namespace': namespace,
                                        'use_sim_time': use_sim_time,
                                        'autostart': autostart,
                                        'use_respawn': use_respawn}.items())])

    ])

    # Create the launch description and populate
    ld = LaunchDescription()

    # Set environment variables
    ld.add_action(stdout_linebuf_envvar)

    # Declare the launch options
    ld.add_action(declare_namespace_cmd)
    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(declare_autostart_cmd)
    ld.add_action(declare_use_respawn_cmd)

    # Add the actions to launch all of the navigation nodes
    ld.add_action(nodes_group)

    return ld
