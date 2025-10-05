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
from launch_ros.actions import SetParametersFromFile
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    namespace = LaunchConfiguration('namespace')
    tf_prefix = LaunchConfiguration('tf_prefix', default=namespace)

    return LaunchDescription([
        DeclareLaunchArgument(
            "namespace",
            default_value=TextSubstitution(text="lr30")
        ),
        DeclareLaunchArgument(
            "tf_prefix",
            default_value=namespace
        ),
        SetParametersFromFile(
          filename=PathJoinSubstitution([
            FindPackageShare('lr30_project11'),
            'config',
            'lr30.yaml'
          ])
        ),
        GroupAction(
            actions=[
                PushROSNamespace(namespace),
                SetParametersFromFile(
                filename=PathJoinSubstitution([
                    FindPackageShare('lr30_project11'),
                    'config',
                    'lr30.yaml'
                ])
                ),
                IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    PathJoinSubstitution([
                    FindPackageShare('project11'),
                    'launch',
                    'robot_core_launch.py'
                    ])
                ),
                launch_arguments={
                    'namespace': namespace,
                    'enable_bridge': 'true',
                    'enable_helm': 'false',
                }.items()
                ),
                # mru_transform Provides tf2 transforms from multiple gps and motion sensor sources.
                Node(
                    package='mru_transform',
                    executable='mru_transform_node',
                    name='mru_transform',
                    emulate_tty=True,
                    parameters=[
                        {'base_frame': [tf_prefix, '/base_link']},
                        {'map_frame': [tf_prefix, '/map']},
                        {'odom_frame': [tf_prefix, '/odom']}
                    ],
                ),
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
                        PushROSNamespace("navigation/sbg"),
                        Node(
                            package="marine_ais_tools",
                            executable="nmea_relay",
                            name="nmea_relay",
                            parameters=[{
                                'input_type': 'udp',
                                'input_port': 5307,
                                'frame_id': 'lr30/sbg',
                            }]
                        ),
                        Node(
                            package="nmea_navsat_driver",
                            executable="nmea_topic_driver",
                            name="nmea_topic_driver",
                            remappings=[('nmea_sentence', 'nmea')],
                        )
                    ]
                )
            ]
        )
    ])
