from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    endpoint_arg = DeclareLaunchArgument('endpoint', default_value='ads1256')
    publish_rate_arg = DeclareLaunchArgument('publish_rate', default_value='10.0')
    frame_id_arg = DeclareLaunchArgument('frame_id', default_value='ads1256')
    simulate_arg = DeclareLaunchArgument('simulate', default_value='false')
    fallback_arg = DeclareLaunchArgument('fallback_to_simulation', default_value='true')

    node = Node(
        package='ads1256',
        executable='run.py',
        name='ads1256_publisher',
        output='screen',
        respawn=True,
        respawn_delay=2.0,
        parameters=[{
            'endpoint': LaunchConfiguration('endpoint'),
            'publish_rate': LaunchConfiguration('publish_rate'),
            'frame_id': LaunchConfiguration('frame_id'),
            'simulate': LaunchConfiguration('simulate'),
            'fallback_to_simulation': LaunchConfiguration('fallback_to_simulation'),
        }],
    )

    return LaunchDescription([
        endpoint_arg,
        publish_rate_arg,
        frame_id_arg,
        simulate_arg,
        fallback_arg,
        node,
    ])
