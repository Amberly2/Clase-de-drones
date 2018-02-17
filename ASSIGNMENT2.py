from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, LocationGlobal 
from pymavlink import mavutil
import tkinter as tk
import time


drone = connect('udp:127.0.0.1:14551', wait_ready=True) #Drone is connected to the computer


def arm_and_takeoff(TargetAltitude): #TargetAltitude is for specifying any altitude in commands

	print("Ready to arm: ", drone.is_armable) #Drone is preapering for arm

	while not drone.is_armable: 
		print ("Vehicle is not armable, waiting...")
		time.sleep(1) #Time sleep works as a delay. Drone stops during the seconds indicated before executing the next instruction.
	drone.mode = VehicleMode("GUIDED") #With GUIDED, drone accepts commands from the computer
	drone.armed = True #Drone motors are on

	print("Vehicle armed")

	while not drone.armed:
		print ("Waiting for arming...")
		time.sleep(1)

	print("Taking off...")
	drone.simple_takeoff(TargetAltitude) #Drone is taking off

	while True:
		Altitude = drone.location.global_relative_frame.alt  #This part defines drone location 
		print("Altitude: ", Altitude)

		if Altitude >= TargetAltitude * 0.95: #0.95 is used because we are using a simulator, and in real life, altitude is not very specific
			print("Altitude reached")
			break
        time.sleep(1)

def set_velocity_body(drone, vx, vy, vz):
	msg = vehicle.message_factory.set_position_target_local_ned_encode(
	        0, 
	        0, 0, 
	        mavutil.mavlink.MAV_FRAME_BODY_NED,
	        0b0000111111000111, #BITMASK
	        0, 0, 0,    #POSITION
	        vx, vy, vz, #VELOCITY
	        0, 0, 0,    #ACCELERATIONS
	        0, 0)
        vehicle.send_mavlink(msg)
        vehicle.flush()

#Key event function
def key(event):
    if event.char == event.keysym:
		if event.keysym == 'r':
			print("r pressed >> Set the vehicle to RTL")
			drone.mode = VehicleMode("RTL")

    else:
        if event.keysym == 'Up':
             set_velocity_body(drone, 5, 0, 0)
        elif event.keysym == 'Down':
             set_velocity_body(drone, -5, 0, 0)
        elif event.keysym == 'Left':
             set_velocity_body(drone, 0, -5, 0)
        elif event.keysym == 'Right':
             set_velocity_body(drone, 0, 5,0)

arm_and_takeoff(20) #Here we indicate altitude

root = tk.Tk()
print("Control the drone with the arrow keys. Press r for RTL mode")
root.bind_all('<Key>', key)
root.mainloop()

