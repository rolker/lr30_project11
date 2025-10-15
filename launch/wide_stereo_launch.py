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
                'camera.width': 1280,
                'camera.height': 720,
                'left_camera_id':  "194430106121872D00",
                'right_camera_id': "19443010D117872D00",
                'left_camera_frame_id': 'lr30/camera_left_optical',
                'right_camera_frame_id': 'lr30/camera_right_optical',
                'ewasr.enabled': False,
                'ewasr_neural_network': PathJoinSubstitution
                ([
                    FindPackageShare("depthai_marine"),
                    "config",
                    "ewasr_resnet18.blob"
                ]),
                'jolo.enabled': True,
                'yolo_neural_network': PathJoinSubstitution([
                    FindPackageShare('depthai_marine'),
                    'config',
                    '1280x704_yolov5_model4_3_openvino_2022.1_6shave.blob'
                ]),
                'yolo_width': 1280,
                'yolo_height': 704,
                'yolo_confidence_threshold': 0.45,
                'yolo_number_of_classes': 2,
                'yolo_anchors': [10.0, 13.0, 16.0, 30.0, 33.0, 23.0, 30.0, 61.0, 62.0, 45.0, 59.0, 119.0, 116.0, 90.0, 156.0, 198.0, 373.0, 326.0],
                'yolo_anchor_mask_labels': ['side160', 'side80', 'side40'],
                'yolo_anchor_masks.side160': [0, 1, 2],
                'yolo_anchor_masks.side80': [3, 4, 5],
                'yolo_anchor_masks.side40': [6, 7, 8],
                'yolo_iou_threshold': 0.5,
            }],
            #emulate_tty=True
            output="screen"
        ),
        # Node(
        #     package="sea_surface_segmentation",
        #     executable="sea_surface_segmentation",
        #     name="sea_surface_segmentation",
        #     parameters=[{
        #         'left_camera_id':  "194430106121872D00",
        #         'right_camera_id': "19443010D117872D00",
        #         'left_camera_frame_id': 'lr30/camera_left_optical',
        #         'right_camera_frame_id': 'lr30/camera_right_optical',
        #         'neural_network': PathJoinSubstitution
        #         ([
        #             FindPackageShare("depthai_marine"),
        #             "config",
        #             "ewasr_resnet18.blob"
        #         ]),
        #         'yolo_blob_path': PathJoinSubstitution([
        #             FindPackageShare('depthai_marine'),
        #             'config',
        #             '1280x704_yolov5_model4_3_openvino_2022.1_6shave.blob'
        #         ]),
        #         'yolo_width': 1280,
        #         'yolo_height': 704,
        #         'yolo_confidence_threshold': 0.5,
        #         'yolo_number_of_classes': 2,
        #         'yolo_anchors': [10.0, 13.0, 16.0, 30.0, 33.0, 23.0, 30.0, 61.0, 62.0, 45.0, 59.0, 119.0, 116.0, 90.0, 156.0, 198.0, 373.0, 326.0],
        #         'yolo_anchor_mask_labels': ['side160', 'side80', 'side40'],
        #         'yolo_anchor_masks.side160': [0, 1, 2],
        #         'yolo_anchor_masks.side80': [3, 4, 5],
        #         'yolo_anchor_masks.side40': [6, 7, 8],
        #         'yolo_iou_threshold': 0.5,
        #     }],
        #     #emulate_tty=True
        #     output="screen"
        # )
    ])
