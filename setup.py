from setuptools import setup
from glob import glob

package_name = 'ads1256'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.py')),
        ('share/' + package_name + '/config', glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=False,
    maintainer='Oleksii Vyshnevskyi',
    maintainer_email='lex.vyshnevskyy@gmail.com',
    description='ROS 2 ADS1256 publisher node for Raspberry Pi / Waveshare hardware.',
    license='TODO',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ads1256_node = ads1256.node:main',
        ],
    },
)
