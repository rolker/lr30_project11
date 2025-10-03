from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import GroupAction
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PathJoinSubstitution
from launch.substitutions import TextSubstitution
from launch_ros.actions import Node
from launch_ros.actions import PushROSNamespace
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    namespace = LaunchConfiguration('namespace')

    return LaunchDescription([
        DeclareLaunchArgument(
            "namespace",
            default_value=TextSubstitution(text="lr30")
        ),
        GroupAction(
            actions=[
                PushROSNamespace(namespace),
                GroupAction(
                    actions=[
                        PushROSNamespace("sensors/cameras"),
                        IncludeLaunchDescription(
                            PythonLaunchDescriptionSource([
                                PathJoinSubstitution([
                                    FindPackageShare("lr30_project11"),
                                    "launch",
                                    "wide_stereo_launch.py"
                                ])
                            ])
                        )
                    ]
                ),
                GroupAction(
                    actions=[
                        PushROSNamespace("navigation"),
                        Node(
                            package="sbg_driver",
                            executable="sbg_device",
                            name="sbg_device",
                            parameters=[
                                PathJoinSubstitution([
                                    FindPackageShare("lr30_project11"),
                                    "config",
                                    "sbg.yaml"
                                ])
                            ]
                        )
                    ]
                )
            ]
        )
    ])
