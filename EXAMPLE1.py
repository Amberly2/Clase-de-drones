from dronekit import connect, VehicleMode, LocationGlobalRelative
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

arm_and_takeoff(20) #Here we indicate altitude

drone.airspeed = 10 #Both commands define speed in air and ground
drone.groundspeed =10

print ("Moving to Point1") #Drone is moving from home to the first point
P1 = LocationGlobalRelative(20.735503, -103.457270, 20) #Tec courts own these coordinates
drone.simple_goto(P1)
time.sleep(30)

print ("Moving to Point2")#Drone now is moving to the second point
P2 = LocationGlobalRelative(20.736278, -103.457218, 20)
drone.simple_goto(P2)
time.sleep(30)

print("Moving to Point3")#Drone is moving to the third point
P3 = LocationGlobalRelative(20.736213, -103.456161, 20)
drone.simple_goto(P3)
time.sleep(30)

print("Returning home") #And now is returning to the initial point. We use RTL to do that,and landing.
drone.mode = VehicleMode ("RTL")
time.sleep(30)
print("Landed")


print("Battery Voltage: %sv" % drone.battery.voltage) #This prints the battery voltage.







