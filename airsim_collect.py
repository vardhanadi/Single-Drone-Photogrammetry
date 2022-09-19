import time

import airsim
import numpy as np


# Set waypoint bounds and parameters for a lawnmower pattern
wp_bound_x = [-500, 500]
wp_bound_y = [-500, 500]
wp_step = 50
wp_z = 150   #50 # height

#low height low step size

# Set initial pose
x = wp_bound_x[0]
y = wp_bound_y[0]
z = wp_z
yaw = 0 * np.pi/180
pitch = -90 * np.pi/180
roll = 0 * np.pi/180

# Connect to AirSim
client = airsim.MultirotorClient()

client.reset()
client.confirmConnection()

# Start recording
client.startRecording()

# === Generate Trajectory (Lawn-Mover Pattern) ===
 
d = 1 # d= 0/1
while y <= wp_bound_y[1]:
    while (d == 0 and x <= wp_bound_x[1]) or (d == 1 and x >= wp_bound_x[0]):

        # Set the pose
        yaw = d * 180 * np.pi/180
        client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(x, -y, -z), airsim.to_quaternion(pitch, -roll, yaw)), True)

        time.sleep(0.1)     # Short delay

        if d == 0:
            x += wp_step
        else:
            x -= wp_step
        print("Step...", x)

    if d == 0:
        x -= wp_step
    else:
        x += wp_step

    d = 1 - d
    y += wp_step

# Stop recording
client.stopRecording()
