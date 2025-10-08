from launch import LaunchDescription

from launch.actions import DeclareLaunchArgument
from launch.actions import GroupAction
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import AnyLaunchDescriptionSource
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PathJoinSubstitution
from launch.substitutions import TextSubstitution

from launch_ros.actions import Node
from launch_ros.actions import PushROSNamespace
from launch_ros.actions import SetParametersFromFile
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    namespace = LaunchConfiguration('namespace')
    robot_namespace = LaunchConfiguration('robot_namespace')

    return LaunchDescription([
        DeclareLaunchArgument(
            "namespace",
            default_value=TextSubstitution(text="operator")
        ),
        DeclareLaunchArgument(
            "robot_namespace",
            default_value=TextSubstitution(text="lr30")
        ),
        DeclareLaunchArgument(
            "background_chart",
            default_value=PathJoinSubstitution([ FindPackageShare('camp'), 'workspace','2025_Erie', 'Erie.pdf'])
        ),
        SetParametersFromFile(
            filename=PathJoinSubstitution([FindPackageShare('lr30_project11'), 'config', 'operator.yaml']),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([FindPackageShare('project11'), '/launch/operator_core_launch.py']),
            launch_arguments={
                'robot_namespace': robot_namespace,
                'enable_bridge': 'true'
            }.items()
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    FindPackageShare('lr30_project11'),
                    'launch',
                    'publish_state_launch.py'
                ])
            ),
            launch_arguments={
                'namespace': robot_namespace
            }.items()
        ),
        GroupAction(
            actions=[
                PushROSNamespace(namespace),
                Node(
                    package="camp",
                    executable="CCOMAutonomousMissionPlanner",
                    name="camp",
                    arguments=[
                        PathJoinSubstitution([ FindPackageShare('camp'), 'workspace']),
                        LaunchConfiguration('background_chart')
                    ],
                    output="screen",
                ),
            ]
        ),
        IncludeLaunchDescription(
            AnyLaunchDescriptionSource(
                PathJoinSubstitution([
                    FindPackageShare('foxglove_bridge'),
                    'launch',
                    'foxglove_bridge_launch.xml'
                ])
            )
        )
    ])
