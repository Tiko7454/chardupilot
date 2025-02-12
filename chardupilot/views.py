from django.shortcuts import render
from .models import Drone


def home(request):
    drone = Drone()
    data = {
        "is_connected": drone.is_connected,
        "is_connected": True,  # for debugging
        "is_ready_to_arm": drone.is_ready_to_arm(),
        "current_mode": drone.get_mode(),
        "alt": drone.get_altitude(),
        "lon": drone.get_longitude(),
        "lat": drone.get_latitude(),
        "logs": drone.logs.dump(),
    }
    return render(request, "home.html", data)
