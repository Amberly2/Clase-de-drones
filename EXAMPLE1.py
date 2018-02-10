from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
drone = connect('udp:127.0.0.1:14551', wait_ready=True)

def arm_and_takeoff(TargetAltitude):

	print("Pre-arm checks...")

	print("Ready to arm: ", drone.is_armable)

	while not drone.is_armable:
		print ("Vehicle is not armable, waiting...")
		time.sleep(1)

	print("WARNING: Arming motors!")

	drone.mode = VehicleMode("GUIDED")
	drone.armed = True

	print("Vehicle armed")

	while not drone.armed:
		print ("Waiting for arming...")
		time.sleep(1)

	print("Taking off...")
	drone.simple_takeoff(TargetAltitude)

	while True:
		Altitude = drone.location.global_relative_frame.alt 
		print("Altitude: ", Altitude)

		if Altitude >= TargetAltitude * 0.95:
			print("Altitude reached")
			break
        time.sleep(1)


def LandDrone():
	print("Landing")
	drone.mode = VehicleMode("LAND")
	while True:
		Altitude = drone.location.global_relative_frame.alt 
		print("Altitude: ", Altitude)

		if Altitude <= 0:
			print("Landed")
			break
		time.sleep(1)

arm_and_takeoff(20)

drone.speed = 10

print ("Moving to Point2")
P2 = LocationGlobalRelative(20.735503, -103.457270, 20)
drone.simple_goto(P2)
time.sleep(30)

print ("Moving to Point3")
P3 = LocationGlobalRelative(20.736278, -103.457218, 20)
drone.simple_goto(P3)
time.sleep(30)

print("Moving to Point4")
P4 = LocationGlobalRelative(20.736213, -103.456161, 20)
drone.simple_goto(P4)
time.sleep(30)

drone.mode = VehicleMode ("RTL")
time.sleep(30)







