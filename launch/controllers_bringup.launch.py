# Copyright 2024, Everardo Gonzalez
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
from launch.actions import RegisterEventHandler, ExecuteProcess, LogInfo
from launch.event_handlers import OnProcessExit
from launch.substitutions import FindExecutable, PathJoinSubstitution, TextSubstitution

from launch_ros.actions import Node

from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    """Generate a launch description to run the chained controller demo.

    Returns:
        The example launch description.
    """
    config_file = PathJoinSubstitution(
        [
            FindPackageShare('unconstrained_mpc_controller_demo'),
            'config',
            'controllers.yaml',
        ]
    )

    control_loop_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        output='both',
        parameters=[config_file],
    )

    set_thruster_hw_component_state_proccess = ExecuteProcess(
        cmd=[
            FindExecutable(name='ros2'),
            'control',
            'set_hardware_component_state',
            'bluerov2_thrusters',
            'active'
        ]
    )

    thruster_spawners = [
        Node(
            package='controller_manager',
            executable='spawner',
            arguments=[
                f'thruster_{i + 1}_controller',
                '--controller-manager',
                ['', 'controller_manager'],
                '--param-file', config_file
            ],
        )
        for i in range(6)
    ]

    delay_thruster_spawners = []
    for i, thruster_spawner in enumerate(thruster_spawners):
        if not len(delay_thruster_spawners):
            delay_thruster_spawners.append(
                thruster_spawner,
            )
        else:
            delay_thruster_spawners.append(
                RegisterEventHandler(
                    event_handler=OnProcessExit(
                        target_action=thruster_spawners[i - 1],
                        on_exit=[thruster_spawner],
                    )
                )
            )

    first_thrust_controller_spawner = delay_thruster_spawners[0]
    set_thruster_hw_component_state_proccess_handler = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=set_thruster_hw_component_state_proccess,
            on_exit=[
                first_thrust_controller_spawner,
                LogInfo(msg='First thruster controller spawned')
            ]
        )
    )

    velocity_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'unconstrained_mpc_controller',
            '--controller-manager',
            ['', 'controller_manager'],
            '--param-file', config_file
        ],
    )

    tam_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'thruster_allocation_matrix_controller',
            '--controller-manager',
            ['', 'controller_manager'],
            '--param-file', config_file
        ],
    )

    delay_tam_controller_spawner_after_thruster_controller_spawners = (
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=thruster_spawners[-1],
                on_exit=[
                    LogInfo(msg='Starting TAM controller spawner'),
                    tam_controller_spawner,
                    LogInfo(
                        msg='Thruster allocation matrix controller spawner executed successfully.'
                    )
                ],
            )
        )
    )

    delay_velocity_controller_spawner_after_tam_controller_spawner = (
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=tam_controller_spawner,
                on_exit=[
                    LogInfo(
                        msg='Starting unconstrained MPC controller spawner'
                    ),
                    velocity_controller_spawner,
                    LogInfo(
                        msg='Unconstrained MPC controller "{}" spawner executed successfully.'
                    )
                ],
            )
        )
    )

    nodes = [
        control_loop_node,
        set_thruster_hw_component_state_proccess,
        set_thruster_hw_component_state_proccess_handler,
        *delay_thruster_spawners[1:],
        delay_tam_controller_spawner_after_thruster_controller_spawners,
        delay_velocity_controller_spawner_after_tam_controller_spawner,
    ]

    return LaunchDescription(nodes)
