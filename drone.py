from dronekit import connect, VehicleMode, Vehicle
import time


class Drone:
    def __init__(self, connection_string):
        self.vehicle: Vehicle = connect(connection_string, wait_ready=True)
        self.has_taken_off = False

    def get_altitude(self):
        return self.vehicle.location.global_relative_frame.alt

    def get_longitude(self):
        return self.vehicle.location.global_relative_frame.lon

    def get_latitude(self):
        return self.vehicle.location.global_relative_frame.lat

    def get_mode(self):
        return self.vehicle.mode

    def _set_mode(self, mode):
        print(f"Switching to {mode} mode")
        self.vehicle.mode = VehicleMode(mode)

    def set_guided_mode(self):
        self._set_mode("GUIDED")

    def set_loiter_mode(self):
        self._set_mode("LOITER")

    def set_return_to_launch_mode(self):
        self._set_mode("RETURN_TO_LAUNCH")

    def set_land_mode(self):
        self._set_mode("LAND")

    def arm(self, force=False):
        if force:
            self._set_mode("GUIDED_NOGPS")

        if not force and self.vehicle.mode != "GUIDED":
            self.set_guided_mode()

        print("Basic pre-arm checks")
        while not force and not self.vehicle.is_armable:
            print("Waiting for vehicle to initialise...")
            time.sleep(1)

        self.vehicle.armed = True
        while not self.vehicle.armed:
            print("Waiting for arming...")
            time.sleep(1)
        print("Drone is armed")

    def disarm(self):
        self.vehicle.armed = False
        while self.vehicle.armed:
            print("Waiting for drone to disarm...")
            time.sleep(1)
        print("Drone is disarmed.")

    def take_off(self, target_altitude):
        if not self.vehicle.armed:
            print("Drone was not armed")
            self.arm()

        if self.vehicle.mode != "GUIDED":
            self.set_guided_mode()

        print("Taking off!")
        self.vehicle.simple_takeoff(target_altitude)

        while True:
            print("Altitude: %s" % self.vehicle.location.global_relative_frame.alt)
            if (
                self.vehicle.location.global_relative_frame.alt
                >= target_altitude * 0.95
            ):
                print("Reached target altitude")
                self.has_taken_off = True
                break
            time.sleep(1)

    def finish(self):
        self.vehicle.close()
