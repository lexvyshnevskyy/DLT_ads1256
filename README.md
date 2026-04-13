# ads1256 (ROS 2)

## External dependencies
This ROS 2 package still expects the target system to provide the hardware-related Python dependencies used by the original project:
- `pipyadc`
- `pigpio`

It also expects the Raspberry Pi SPI/GPIO wiring used by the Waveshare ADS1256 board.

## Run
```bash
ros2 launch ads1256 ads1256.launch.py
```
