import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import UnlessCondition, IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    is_sim_arg = DeclareLaunchArgument(
        "is_sim",
        default_value="True"
    )

    use_python_arg = DeclareLaunchArgument(
        "use_python",
        default_value="False",
    )

    use_python = LaunchConfiguration("use_python")
    is_sim = LaunchConfiguration("is_sim")

    task_server_node = Node(
        package="arduinobot_remote",
        executable="task_server_node",
        condition=UnlessCondition(use_python),
        parameters=[{"use_sim_time": is_sim}]
    )

    # Get absolute paths to files
    urdf_file = os.path.join(
        get_package_share_directory("arduinobot_description"),
        "urdf",
        "arduinobot.urdf.xacro"
    )
    
    srdf_file = os.path.join(
        get_package_share_directory("arduinobot_moveit"),
        "config",
        "arduinobot.srdf"
    )
    
    controllers_file = os.path.join(
        get_package_share_directory("arduinobot_moveit"),
        "config",
        "moveit_controllers.yaml"
    )

    # Create MoveIt config with explicit paths
    moveit_config = (
        MoveItConfigsBuilder("arduinobot", package_name="arduinobot_moveit")
        .robot_description(file_path=urdf_file)
        .robot_description_semantic(file_path=srdf_file)
        .trajectory_execution(file_path=controllers_file)
        .to_moveit_configs()
    )

    # MoveIt move_group node
    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            moveit_config.to_dict(),
            {"use_sim_time": is_sim},
            {"publish_robot_description_semantic": True}
        ],
        arguments=["--ros-args", "--log-level", "info"],
    )

    task_server_node_py = Node(
        package="arduinobot_remote",
        executable="task_server.py",
        condition=IfCondition(use_python),
        parameters=[moveit_config.to_dict(),
                    {"use_sim_time": is_sim}]
    )

    return LaunchDescription([
        use_python_arg,
        is_sim_arg,
        task_server_node,
        move_group_node,
        # task_server_node_py,
    ])



# ---------------------------------------------
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import UnlessCondition, IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    is_sim_arg = DeclareLaunchArgument(
        "is_sim",
        default_value="True"
    )

    use_python_arg = DeclareLaunchArgument(
        "use_python",
        default_value="False",
    )

    use_python = LaunchConfiguration("use_python")
    is_sim = LaunchConfiguration("is_sim")

    task_server_node = Node(
        package="arduinobot_remote",
        executable="task_server_node",
        condition=UnlessCondition(use_python),
        parameters=[{"use_sim_time": is_sim}]
    )

    moveit_config = (
        MoveItConfigsBuilder("arduinobot", package_name="arduinobot_moveit")
        .robot_description(file_path=os.path.join(
            get_package_share_directory("arduinobot_description"),
            "urdf",
            "arduinobot.urdf.xacro"
            )
        )
        .robot_description_semantic(file_path=os.path.join(
            get_package_share_directory("arduinobot_moveit"),
            "config",
            "arduinobot.srdf"
            )   
        )
        # .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .trajectory_execution(file_path=os.path.join(
            get_package_share_directory("arduinobot_moveit"),
            "config",
            "moveit_controllers.yaml"
            )   
        )
        # .moveit_cpp(file_path="config/planning_python_api.yaml")
        .to_moveit_configs()
    )

# MoveIt move_group node
    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            moveit_config.to_dict(),
            {"use_sim_time": is_sim},
            {"publish_robot_description_semantic": True}
        ],
        arguments=["--ros-args", "--log-level", "info"],
    )

    task_server_node_py = Node(
        package="arduinobot_remote",
        executable="task_server.py",
        condition=IfCondition(use_python),
        parameters=[moveit_config.to_dict(),
                    {"use_sim_time": is_sim}]
    )

 

    return LaunchDescription([
        use_python_arg,
        is_sim_arg,
        task_server_node,
        move_group_node,
        # task_server_node_py,
    ])

#-------------------------------------------


#CPP Only Node  - attempting top see if this works 

# import os
# from launch import LaunchDescription
# from launch.actions import DeclareLaunchArgument
# from launch.conditions import UnlessCondition
# from launch.substitutions import LaunchConfiguration, Command
# from launch_ros.actions import Node
# from ament_index_python.packages import get_package_share_directory


# def generate_launch_description():

#     is_sim_arg = DeclareLaunchArgument(
#         "is_sim",
#         default_value="True"
#     )

#     use_python_arg = DeclareLaunchArgument(
#         "use_python",
#         default_value="False",
#     )

#     use_python = LaunchConfiguration("use_python")
#     is_sim = LaunchConfiguration("is_sim")

#     robot_state_publisher_node = Node(
#         package="robot_state_publisher",
#         executable="robot_state_publisher",
#         name="robot_state_publisher",
#         parameters=[{
#             "robot_description": Command([
#                 "xacro ",
#                 os.path.join(
#                     get_package_share_directory("arduinobot_description"),
#                     "urdf",
#                     "arduinobot.urdf.xacro"
#                 )
#             ]),
            
#             "use_sim_time": is_sim
#         }]
#     )

#     task_server_node = Node(
#         package="arduinobot_remote",
#         executable="task_server_node",
#         condition=UnlessCondition(use_python),
#         parameters=[{
#             "use_sim_time": is_sim,
#             "robot_description_semantic": open(
#                 "/home/nicholas/arduinobot_ws/install/arduinobot_moveit/share/arduinobot_moveit/config/arduinobot.srdf"
#             ).read()
#         }]
# )

#     return LaunchDescription([
#         use_python_arg,
#         is_sim_arg,
#         robot_state_publisher_node,
#         task_server_node,
#     ])