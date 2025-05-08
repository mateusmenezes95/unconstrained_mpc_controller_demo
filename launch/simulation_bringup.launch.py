# MIT License
# 
# Copyright (c) 2025 Mateus Menezes
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, LogInfo
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution

from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    """Generate a launch description to run the chained controller demo.

    Returns:
        The example launch description.
    """
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name='xacro')]),
            ' ',
            PathJoinSubstitution(
                [
                    FindPackageShare('unconstrained_mpc_controller_demo'),
                    'description',
                    'urdf',
                    'bluerov2.config.xacro',
                ]
            ),
            ' ',
            'use_sim:=true',
        ]
    )

    log_robot_description = LogInfo(
        msg=robot_description_content
    )

    blue_bringup_launch = IncludeLaunchDescription(
        PathJoinSubstitution(
            [
                FindPackageShare('blue_bringup'),
                'launch',
                'bluerov2',
                'bluerov2.launch.yaml'
            ]
        ),
        launch_arguments={
            'robot_description': robot_description_content,
            'use_sim': 'true',
        }.items()
    )

    return LaunchDescription(
        [
            log_robot_description,
            blue_bringup_launch,
        ]
    )
