from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import GroupAction
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PathJoinSubstitution
from launch.substitutions import PythonExpression
from launch.substitutions import TextSubstitution
from launch_ros.actions import Node
from launch_ros.actions import PushROSNamespace
from launch_ros.actions import SetParameter
from launch_ros.actions import SetParametersFromFile
from launch_ros.actions import SetRemap
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
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    FindPackageShare('lr30_project11'),
                    'launch',
                    'publish_state_launch.py'
                ])
            ),
            launch_arguments={
                'namespace': namespace
            }.items()
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
                        'enable_helm': 'false',
                    }.items()
                ),
                IncludeLaunchDescription(
                    PythonLaunchDescriptionSource(
                        PathJoinSubstitution([
                            FindPackageShare('udp_bridge'),
                            'launch',
                            'udp_bridge_launch.py'
                        ])
                    )
                ),
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
                Node(
                    package='mission_manager',
                    executable='multibeam_coverage_adapter',
                    name='multibeam_coverage_adapter',
                    emulate_tty=True,
                ),
                IncludeLaunchDescription(
                    PythonLaunchDescriptionSource(
                        PathJoinSubstitution([
                            FindPackageShare('manda_coverage'),
                            'launch',
                            'manda_coverage_launch.py'
                        ])
                    )
                ),
                GroupAction(
                    actions=[
                        PushROSNamespace("sensors"),
                        IncludeLaunchDescription(
                            PythonLaunchDescriptionSource([
                                PathJoinSubstitution([
                                    FindPackageShare("lr30_project11"),
                                    "launch",
                                    "sonar_launch.py"
                                ])
                            ])
                        ),
                        GroupAction(
                            actions=[
                                PushROSNamespace("sonar"),
                                GroupAction(
                                    actions=[
                                        SetParameter(
                                            name='sensors.sbg.topics.orientation',
                                            value=PythonExpression( expression = [ '"/', 
                                                namespace, '/navigation/sbg/orientation"'
                                            ])
                                        ),
                                        SetParameter(
                                            name='sensors.sbg.topics.position',
                                            value=PythonExpression( expression = [ '"/',
                                                namespace, '/navigation/sbg/fix"'
                                            ])
                                        ),
                                        SetParameter(
                                            name='sensors.sbg.topics.velocity',
                                            value=PythonExpression( expression = [ '"/',
                                                namespace, '/navigation/sbg/vel"'
                                            ])
                                        ),
                                        IncludeLaunchDescription(
                                            PythonLaunchDescriptionSource(
                                                PathJoinSubstitution([
                                                    FindPackageShare('cube_bathymetry'),
                                                    'launch',
                                                    'detections_to_pointcloud_launch.py'
                                                ])
                                            )
                                        ),
                                    ]
                                ),
                                GroupAction(
                                    actions=[
                                    SetParameter(
                                        name='map_frame',
                                        value=PythonExpression(
                                            expression = ['"', tf_prefix, '/map"']
                                        )
                                    ),
                                    SetParameter(
                                        name='cell_size',
                                        value=1.0
                                    ),
                                    IncludeLaunchDescription(
                                        PythonLaunchDescriptionSource(
                                            PathJoinSubstitution([
                                                FindPackageShare('cube_bathymetry'),
                                                'launch',
                                                'cube_bathymetry_launch.py'
                                            ])
                                        )
                                    ),
                                    ]
                                )
                            ]
                        ),

                    ]
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
