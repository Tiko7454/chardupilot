from collections import deque
from typing import Optional
from singleton_decorator import singleton
from dronekit import connect, VehicleMode, Vehicle
import time


class Logs:
    def __init__(self) -> None:
        self.content = deque()

    def add_log(self, text, color) -> None:
        self.content.append(self.Log(text, color))
        while len(self.content) > 3:
            self.content.popleft()

    class Log:
        def __init__(self, text="", color="white") -> None:
            self.text = text
            self.color = color

        def dump(self):
            return (self.text, self.color)

    def dump(self):
        return [log.dump() for log in (list(self.content) + [self.Log()] * 3)]


@singleton
class Drone:
    def __init__(self, connection_string=None, baud="0"):
        self.__sleep_time = 0.2
        self.logs = Logs()
        self.vehicle: Optional[Vehicle] = None
        if not connection_string:
            self.is_connected = False
            self._set_home()
            return
        self.connect(connection_string, baud)
        self._set_home()

    def _wait(self):
        time.sleep(self.__sleep_time)

    def _get_coordinates(self):
        return (self.get_altitude(), self.get_longitude(), self.get_latitude())

    def _set_home(self):
        self.home = self._get_coordinates()

    def connect(self, connection_string, baud: str):
        self.vehicle = connect(connection_string, wait_ready=True, baud=int(baud))
        self.has_taken_off = False
        self.is_connected = True

    def disconnect(self):
        self.vehicle.close()
        self.is_connected = False

    def is_ready_to_arm(self):
        if self.vehicle:
            return self.vehicle.is_armable
        return False

    def get_altitude(self):
        if self.vehicle:
            return self.vehicle.location.global_relative_frame.alt
        return 0

    def get_longitude(self):
        if self.vehicle:
            return self.vehicle.location.global_relative_frame.lon
        return 0

    def get_latitude(self):
        if self.vehicle:
            return self.vehicle.location.global_relative_frame.lat
        return 0

    def get_mode(self):
        if self.vehicle:
            return self.vehicle.mode
        return "NOT CONNECTED"

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
            self._wait()

        self.vehicle.armed = True
        while not self.vehicle.armed:
            print("Waiting for arming...")
            self._wait()
        print("Drone is armed")

    def disarm(self):
        self.vehicle.armed = False
        while self.vehicle.armed:
            print("Waiting for drone to disarm...")
            self._wait()
        print("Drone is disarmed.")

    def takeoff(self, target_altitude):
        if not self.vehicle.armed:
            print("Drone was not armed")
            self.arm()

        if self.vehicle.mode != "GUIDED":
            self.set_guided_mode()

        print("Taking off!")
        self._set_home()
        self.vehicle.simple_takeoff(target_altitude)

        while True:
            print(f"Altitude: {self.get_altitude()}")
            if self.get_altitude() >= target_altitude * 0.95:
                print("Reached target altitude")
                self.has_taken_off = True
                break
            self._wait()
