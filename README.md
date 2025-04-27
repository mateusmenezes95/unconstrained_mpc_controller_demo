# Unconstrained MPC Controller Demo

The goal of this package is to provide a demo of the [unconstrained_mpc_controller] package. It contains a set of launch files and configuration files to run the controller with the [BlueROV2] simulated in Gazebo using the [Blue Project].

## Installing dependencies

You can follow two approaches to install the dependencies of the package. The first one is to use the development environment provided by the [Blue Project]. The second one is to install the dependencies manually. The first approach is highly recommended, since it will save you a lot of time and effort. However, if you prefer to install the dependencies manually, you can follow the instructions in the sections below. 

### Using Blue Project

Please follow the instructions [here](https://robotic-decision-making-lab.github.io/blue/installation/) to setup a docker container with the Blue repositories and its dependencies.

After that, clone the repository in your workspace:

```bash
cd ~/ws_blue/src
git clone https://github.com/mateusmenezes95/unconstrained_mpc_controller_demo.git
cd ~/ws_blue
```

> **Note:** The `~/ws_blue` folder is the workspace created by the Blue Project. If you are using a different workspace, please replace `~/ws_blue` with the path to your workspace.

Once you have cloned the repository, pull the source dependencies:

```bash
cd ~/ws_blue/src/
vcs import unconstrained_mpc_controller_demo/dependencies.repos
```

Then, install the binary dependencies:

```bash
rosdep update
sudo apt install update
cd ~/ws_blue
rosdep install --from-paths src/unconstrained_mpc_controller_demo --ignore-src -r -y --rosdistro jazzy
```

### Manual installation

The steps below will help you to install the dependencies of the package.

> **Note:** The steps thereafter assumes that you have installed ROS 2 Jazzy Jalisco. If you have not installed it yet, please follow the instructions [here](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debians.html).

### Tools

It is advised to install the following tools to help you with the installation and building of the package:

- [vcstool](https://github.com/dirk-thomas/vcstool?tab=readme-ov-file#how-to-install-vcstool): Used to clone source dependencies.
- [rosdep](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Rosdep.html#rosdep-installation): Used to install binary dependencies.
- [colcon-mixin-repository](https://github.com/colcon/colcon-mixin-repository?tab=readme-ov-file#how-to-fetch-the-information)

### Installing source dependencies

```bash
cd ~/<your_workspace>/src
vcs import unconstrained_mpc_controller/dependencies.repos
```

### Installing binary dependencies

```bash
rosdep update
sudo apt install update
cd ~/<your_workspace>
rosdep install --from-paths src/unconstrained_mpc_controller --ignore-src -r -y --rosdistro jazzy
```

> run rosdep install --help to see all the options available.

## Building

Once you have cloned the repository in your workspace, you can build it following the steps thereafter:

```bash
cd ~/<your_workspace>
source /opt/ros/jazzy/setup.bash
colcon build --packages-up-to unconstrained_mpc_controller --event-handlers console_direct+ --mixin compile-commands
```

> **Note:** The `--mixin compile-commands` option is used to generate the `compile_commands.json` file, which is useful for IDEs like VSCode and CLion. If you are not using an IDE, you can omit this option.

## Usage

[Blue Project]: https://robotic-decision-making-lab.github.io/blue/
[unconstrained_mpc_controller]: https://github.com/mateusmenezes95/unconstrained_mpc_controller
[BlueROV2]: https://bluerobotics.com/store/rov/bluerov2/
