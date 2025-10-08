from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    return LaunchDescription([
        Node(
            package="depthai_marine",
            executable="wide_stereo",
            name="wide_stereo",
            parameters=[{
                'left_camera_id':  "194430106121872D00",
                'right_camera_id': "19443010D117872D00",
                'left_camera_frame_id': 'lr30/camera_left_optical',
                'right_camera_frame_id': 'lr30/camera_right_optical',
            }],
            #emulate_tty=True
            output="screen"
        )
    ])
