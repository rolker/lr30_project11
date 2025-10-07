from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    return LaunchDescription([
        Node(
            package="r2sonic",
            executable="r2sonic_node",
            name="sonar",
            parameters=[{
                'ports/bathy': 4020,
                'tx_frame_id': 'lr30/sonar',
                'rx_frame_id': 'lr30/sonar',
            }],
            #emulate_tty=True
            output="screen"
        )
    ])
