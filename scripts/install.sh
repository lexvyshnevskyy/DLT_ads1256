#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="${WORKSPACE:-$HOME/ros2_delatometry}"
ROS_SETUP="${ROS_SETUP:-/opt/ros/jazzy/setup.bash}"
VENV_DIR="${VENV_DIR:-$HOME/venvs/ros2_delatometry_webui}"
ENABLE_SPI="${ENABLE_SPI:-0}"
START_PIGPIOD="${START_PIGPIOD:-1}"

echo "[ads1256 install] workspace: $WORKSPACE"
echo "[ads1256 install] ROS setup:  $ROS_SETUP"
echo "[ads1256 install] venv:       $VENV_DIR"

if [ ! -d "$WORKSPACE/src/ads1256" ]; then
  echo "ERROR: package directory not found: $WORKSPACE/src/ads1256"
  exit 1
fi

if [ ! -f "$ROS_SETUP" ]; then
  echo "ERROR: ROS setup file not found: $ROS_SETUP"
  exit 1
fi

echo "[ads1256 install] installing apt dependencies"
sudo apt update
sudo apt install -y \
  python3-venv \
  python3-pip \
  python3-dev \
  build-essential \
  python3-spidev \
  pigpio \
  python3-pigpio \
  raspi-config || true

if [ "$ENABLE_SPI" = "1" ]; then
  echo "[ads1256 install] enabling SPI"
  sudo raspi-config nonint do_spi 0 || true
fi

if [ "$START_PIGPIOD" = "1" ]; then
  echo "[ads1256 install] enabling pigpiod"
  sudo systemctl enable pigpiod || true
  sudo systemctl start pigpiod || true
fi

sudo usermod -aG spi,gpio "$USER" || true

echo "[ads1256 install] creating/updating venv"
python3 -m venv --system-site-packages "$VENV_DIR"
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -r "$WORKSPACE/src/ads1256/requirements.txt"

echo "[ads1256 install] source ROS"
set +u
# shellcheck disable=SC1090
source "$ROS_SETUP"
set -u

echo "[ads1256 install] ensure run.py executable"
chmod +x "$WORKSPACE/src/ads1256/ads1256/run.py"

echo "[ads1256 install] clean build/install"
rm -rf "$WORKSPACE/build/ads1256" "$WORKSPACE/install/ads1256"

echo "[ads1256 install] build with colcon"
cd "$WORKSPACE"
colcon build --symlink-install --packages-select ads1256

echo "[ads1256 install] source workspace"
set +u
# shellcheck disable=SC1090
source "$WORKSPACE/install/setup.bash"
set -u

echo "[ads1256 install] verify"
python3 -c "import pipyadc; print('pipyadc OK')"
python3 -c "import spidev; print('spidev OK')"
python3 -c "import pigpio; print('pigpio OK')"
python3 -c "import ads1256.node; print('ads1256.node OK')"
python3 -c "from msgs.msg import Ads; print('msgs/msg/Ads OK')"

if ! ros2 pkg executables ads1256 | grep -qE '^ads1256[[:space:]]+run.py$'; then
  echo "ERROR: expected executable not found: ads1256 run.py"
  ros2 pkg executables ads1256 || true
  exit 2
fi

echo
echo "[ads1256 install] OK"
echo
echo "Simulation test:"
echo "  cd $WORKSPACE"
echo "  source $ROS_SETUP"
echo "  source $WORKSPACE/install/setup.bash"
echo "  source $VENV_DIR/bin/activate"
echo "  ros2 launch ads1256 ads1256.launch.py simulate:=true"
echo
echo "Hardware test:"
echo "  ros2 launch ads1256 ads1256.launch.py simulate:=false fallback_to_simulation:=false"
echo
echo "If user was newly added to spi/gpio groups, reboot before hardware mode."
