# ads1256 ROS 2 port

This bundle contains a ROS 2 refactor of the original ROS 1 `ads1256` package plus the `msgs` interface package it depends on.

## Packages
- `msgs`: ROS 2 interface package with `Ads.msg` and `E720.msg`
- `ads1256`: ROS 2 `ament_python` package wrapping the ADS1256 reader and publisher node

## Notes
- The ROS node was migrated from `rospy` to `rclpy`.
- The original XML launch file was replaced with a ROS 2 Python launch file.
- External hardware dependencies such as `pipyadc`, `pigpio`, and Raspberry Pi SPI/GPIO setup are still required on the target system.
