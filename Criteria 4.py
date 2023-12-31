#!/usr/bin/env python3
import rclpy
from inputimeout import inputimeout
from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped
import tf_transformations

def create_pose_stamped(navigator, position_x, position_y, rotation_z):
    q_x, q_y, q_z, q_w = tf_transformations.quaternion_from_euler(0.0, 0.0, rotation_z)
    goal_pose = PoseStamped()
    goal_pose.header.frame_id = 'map'
    goal_pose.header.stamp = navigator.get_clock().now().to_msg()
    goal_pose.pose.position.x = position_x
    goal_pose.pose.position.y = position_y
    goal_pose.pose.position.z = 0.2
    goal_pose.pose.orientation.x = q_x
    goal_pose.pose.orientation.y = q_y
    goal_pose.pose.orientation.z = q_z
    goal_pose.pose.orientation.w = q_w
    return goal_pose




def main():
    # --- Init ROS2 communications and Simple Commander API ---
    rclpy.init()
    nav = BasicNavigator()
    li=[]
    
    

    def table_confirmation(nav):
        while not nav.isTaskComplete():
                feedback = nav.getFeedback()
                cancellation = input("Do you wanna cancel?")
                if cancellation == 'y':
                    nav.cancelTask()
                    waypoints = [kitchen,robo_hp]
                    nav.followWaypoints(waypoints)
                    exit()
                else:
                    pass
                print("Task ongoing")
        try:
            global time_over
            time_over = inputimeout(prompt='Please confirm your order:', timeout=5)
            li.append(time_over)
            print("Order confirmed")
        except Exception:
            # Declare the timeout statement
            cancel_table = input("Are you cancelling the order? ")
            if cancel_table == "y":
                print("Order has been cancelled from table ",n[i])
                time_over = 'n'
                li.append(time_over)
                print('Your time is over!')
    
    def kitchen_confirmation(nav):
        while not nav.isTaskComplete():
                feedback = nav.getFeedback()
                cancellation = input("Do you wanna cancel?")
                if cancellation == 'y':
                    nav.cancelTask()
                    nav.goToPose(robo_hp)
                    exit()
                else:
                    pass
                print("Approching kitchen")
        try:
            global time_confi
            time_confi = inputimeout(prompt='Hi chef , Need your confirmation:', timeout=5)
            print("Order confirmed")
        except Exception:
            # Declare the timeout statement
            time_confi = 'n'
            print('Your time is over!')

        

    # --- Set initial pose ---
    initial_pose = create_pose_stamped(nav, 0.1 , -0.4 , 0.0)
    nav.setInitialPose(initial_pose)

    # --- Wait for Nav2 ---
    nav.waitUntilNav2Active()

    # --- Create some Nav2 goal poses ---
    kitchen = create_pose_stamped(nav, 1.6 ,-3.9 , -0.7)
    table_1 = create_pose_stamped(nav, -2.2 , 0.7 ,-0.7)
    table_2 = create_pose_stamped(nav, -4.4 ,0.7 ,-0.4)
    table_3 = create_pose_stamped(nav,-2.5 , -0.9 , 0.9)
    robo_hp = create_pose_stamped(nav, 0.1 , -0.4 , -0.7)


    # nav.goToPose(kitchen)
    # kitchen_confirmation(nav)
        
    # if time_confi == "y":
    #     pass
    # else:
    #     nav.goToPose(robo_hp)
    #     while not nav.isTaskComplete():
    #         feedback = nav.getFeedback()
    #         print("Returning home since no confirmation from the kitchen")
        
        
    

    n = input("Place your order").split()

    nav.goToPose(kitchen)
    kitchen_confirmation(nav)

    if time_confi =='n':
        cancel = input("Are you cancelling the order? ")
        if cancel=="y":
            nav.goToPose(robo_hp)
            while not nav.isTaskComplete():
                print("returning to the home position since order cancelled!")
        exit()

        

    for i in range(len(n)):
        print(i)
        if n[i] == '1':
            nav.goToPose(table_1)
            table_confirmation(nav)
            
        elif n[i] == '2':
            nav.goToPose(table_2)
            table_confirmation(nav)
            
        elif n[i] == '3':
            nav.goToPose(table_3)
            table_confirmation(nav)
            
        else : 
            print("SORRY DEIVA , KEEP TRYING YOU CAN .....")
            

    while not nav.isTaskComplete():
        feedback = nav.getFeedback()
        print(feedback)
    if "n" in li:
        waypoints = [kitchen,robo_hp]
        nav.followWaypoints(waypoints)
    else:
        nav.goToPose(robo_hp)

    # --- Get the result ---
    print(nav.getResult())

    # --- Shutdown ROS2 communications ---
    rclpy.shutdown()

if __name__ == '__main__':
    main()
