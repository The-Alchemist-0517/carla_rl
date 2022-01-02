import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name=='nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla
# Import the library Transform used to explicitly spawn an actor
# from carla import Transform, Location, Rotation
# from carla import Map
# from carla import Vector3D
# To import a basic agent
from agents.navigation.basic_agent import BasicAgent


import random
import time
TOWN = 'Town05'


actor_list = []

# --------------------------------Initialization-----------------------------------#
try:


    ##General connection to server and get blue_print
    client = carla.Client('localhost', 2000)
    client.set_timeout(5.0)

    world = client.load_world(TOWN)
    mp = world.get_map()  # get the map of the current world.
    blueprint_library = world.get_blueprint_library()

    ##Search for specific actor and get its blueprint.
    vehicle_bp1 = blueprint_library.filter('tt')[0]
    vehicle_bp2 = blueprint_library.filter('model3')[0]

    ##Change the color of the actors (attribute)
    vehicle_bp1.set_attribute('color', '255,255,255')  # change the color to white
    vehicle_bp2.set_attribute('color', '0,0,0')

    ##Spawn an actor at specified point by using Transform
    # lag Vehicle
    spawn_point_v1 = carla.Transform(carla.Location(x=-145, y=6.7, z=11),
        carla.Rotation(pitch=0, yaw=0, roll=0))

    # Lead Vehicle
    spawn_point_v2 = carla.Transform(carla.Location(x=-105, y=-4.2, z=11),
        carla.Rotation(pitch=0, yaw=180.5, roll=0))

    vehicle1 = world.spawn_actor(vehicle_bp1, spawn_point_v1)
    vehicle2 = world.spawn_actor(vehicle_bp2, spawn_point_v2)

    actor_list.append(vehicle1)
    actor_list.append(vehicle2)
    ##Keep the leading vehicle static
    # vehicle2.apply_control(carla.VehicleControl(throttle=0.2, steer=0.0, brake=0, hand_brake=True)),

    # agent = BasicAgent(vehicle2)
    # destination_v2 = carla.Transform(carla.Location(x=-135, y=-5, z=11),carla.Rotation(pitch=0, yaw=0, roll=0)),
    # agent.set_destination(destination_v2)

    spectator = world.get_spectator()
    transform = vehicle1.get_transform()
    spectator.set_transform(carla.Transform(transform.location + carla.Location(z=50),
        carla.Rotation(pitch=-90)))

    # ---------------------------------Control Part------------------------------------#
    while True:
        x_v1 = vehicle1.get_location().x
        x_v2 = vehicle2.get_location().x

        y_v1 = vehicle1.get_location().y
        y_v2 = vehicle2.get_location().y

        print(abs(x_v1 - x_v2))
        print(abs(y_v1 - y_v2))


        if abs(x_v1-x_v2) > 5:
            vehicle2.apply_control(carla.VehicleControl(throttle=0.5, steer=0.0))
        else :
             vehicle2.apply_control(carla.VehicleControl(throttle=0, steer=0.0))




        # if abs(x_v2 - x_v1) > 12:  # Drive with "safe distance"
        #     # Control the vehicle:
        #     vehicle1.apply_control(carla.VehicleControl(throttle=0, steer=0.0))
        #
        # elif abs(x_v2 - x_v1) <= 12:  # When the lag vehicle  leave the "safe zone"
        #
        #     while True:
        #         y_v1 = vehicle1.get_location().y
        #         y_v2 = vehicle2.get_location().y
        #
        #         # lag vehicle turn left.
        #         vehicle1.apply_control(carla.VehicleControl(throttle=0, steer=0))
        #         # if the rotation angle is too big, change the direction of steer
        #         if abs(y_v1 - y_v2) > 2:
        #             vehicle1.apply_control(carla.VehicleControl(throttle=0, steer=0))
        #             break
        #
        #     while True:
        #         x_v1 = vehicle1.get_location().x
        #         x_v2 = vehicle2.get_location().x
        #
        #         if abs(x_v1 - x_v2) < 1.0:
        #             # The number in this if statement depends on the safe distance set before.
        #             vehicle1.apply_control(carla.VehicleControl(throttle=0, steer=0.0))
        #             if abs(x_v1 - x_v2) > 25:
        #                 break
        #
        #     break
        time.sleep(1)

finally:
    for actor in actor_list:
        actor.destroy()
    print("All cleaned up!")




