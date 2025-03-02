from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Drone
import datetime

connected = True


def home(request):
    drone = Drone()
    data = {
        "is_connected": drone.is_connected,
        # "is_connected": connected,  # for debugging
        "is_ready_to_arm": get_is_ready_to_arm_string(drone),
        "current_mode": get_mode(request),
        "logs": drone.logs.dump(),
    }
    return render(request, "home.html", data)


def get_is_ready_to_arm_string(drone):
    ready_to_arm = "Ready to Arm"
    if not drone.is_ready_to_arm():
        ready_to_arm = f"Not {ready_to_arm}"
    return ready_to_arm


def dynamic_time(request):
    return HttpResponse(f"{datetime.datetime.now()}")


def get_mode(requiest):
    drone = Drone()
    return HttpResponse(f"{drone.get_mode()}")


def change_to_guided(request):
    drone = Drone()
    drone.set_guided_mode()
    return HttpResponse(f"{drone.get_mode()}")


def change_to_takeoff(request):
    drone = Drone()
    target_altitude = request.GET.get("target-altitude", 0)
    drone.takeoff(target_altitude)
    return HttpResponse(f"{drone.get_mode()}")


def change_to_loiter(request):
    drone = Drone()
    drone.set_loiter_mode()
    return HttpResponse(f"{drone.get_mode()}")


def change_to_return(request):
    drone = Drone()
    drone.set_return_to_launch_mode()
    return HttpResponse(f"{drone.get_mode()}")


def change_to_land(request):
    drone = Drone()
    drone.set_land_mode()
    return HttpResponse(f"{drone.get_mode()}")


def change_armed(request):
    drone = Drone()
    drone.arm()
    return get_ready_to_arm(request)


def change_disarmed(request):
    drone = Drone()
    drone.disarm()
    return get_ready_to_arm(request)


def get_coordinates(request):
    drone = Drone()
    return HttpResponse(
        f"""
            <label>alt: {drone.get_altitude()}</label>
            <label>lon: {drone.get_longitude()}</label>
            <label>lat: {drone.get_latitude()}</label>
            <br>
            <br>
            Home` 
            <label>alt: {drone.home[0]}</label>
            <label>lon: {drone.home[1]}</label>
            <label>lat: {drone.home[2]}</label>
        """
    )


def get_ready_to_arm(request):
    drone = Drone()
    return HttpResponse(get_is_ready_to_arm_string(drone))


def disconnect(request):
    global connected
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)
    drone = Drone()
    connected = False
    drone.disconnect()
    return JsonResponse({"response": "disconnected"})


def connect(request):
    global connected
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)
    drone = Drone()
    connected = True
    connection_string = request.POST.get("connection-string", "")
    baud = request.POST.get("baud", "0")
    drone.connect(connection_string, baud)
    return JsonResponse({"response": "connected"})
