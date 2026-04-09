from typing import Any, Dict

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from msgs.msg import Ads

from .waveshare import AdsData


class Ads1256Publisher(Node):
    def __init__(self) -> None:
        super().__init__('ads1256')

        self.declare_parameter('publish_rate', 10.0)
        self.declare_parameter('endpoint', 'ads1256')
        self.declare_parameter('frame_id', 'ads1256')

        self.publish_rate = float(self.get_parameter('publish_rate').value)
        self.endpoint = str(self.get_parameter('endpoint').value)
        self.frame_id = str(self.get_parameter('frame_id').value)

        self.controller = AdsData()
        self.publisher_ = self.create_publisher(Ads, self.endpoint, 10)

        period = 1.0 / self.publish_rate if self.publish_rate > 0.0 else 0.1
        self.timer = self.create_timer(period, self._on_timer)

        self.get_logger().info(
            f'Started ADS1256 publisher: topic={self.endpoint}, rate={self.publish_rate} Hz, frame_id={self.frame_id}'
        )

    def _on_timer(self) -> None:
        try:
            data = self.controller.poll_data()
            msg = self._parse_response(data)
            self.publisher_.publish(msg)
        except Exception as exc:
            self.get_logger().error(f'Error in ADS1256 polling/publish cycle: {exc}')

    def _parse_response(self, data: Dict[str, Any]) -> Ads:
        response = Ads()
        response.header.stamp = self.get_clock().now().to_msg()
        response.header.frame_id = self.frame_id

        response.AIN0 = int(data.get('AIN0', 0))
        response.AIN1 = int(data.get('AIN1', 0))
        response.AIN2 = int(data.get('AIN2', 0))
        response.AIN3 = int(data.get('AIN3', 0))
        response.AIN4 = int(data.get('AIN4', 0))
        response.AIN5 = int(data.get('AIN5', 0))
        response.AIN6 = int(data.get('AIN6', 0))
        response.AIN7 = int(data.get('AIN7', 0))

        response.ch0 = Float32(data=float(data.get('ch0', 0.0)))
        response.ch1 = Float32(data=float(data.get('ch1', 0.0)))
        response.ch2 = Float32(data=float(data.get('ch2', 0.0)))
        response.ch3 = Float32(data=float(data.get('ch3', 0.0)))
        response.ch4 = Float32(data=float(data.get('ch4', 0.0)))
        response.ch5 = Float32(data=float(data.get('ch5', 0.0)))
        response.ch6 = Float32(data=float(data.get('ch6', 0.0)))
        response.ch7 = Float32(data=float(data.get('ch7', 0.0)))
        return response


def main(args=None) -> None:
    rclpy.init(args=args)
    node = Ads1256Publisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
