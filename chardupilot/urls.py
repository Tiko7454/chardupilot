"""
URL configuration for chardupilot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from .views import (
    home,
    dynamic_time,
    get_mode,
    get_coordinates,
    get_ready_to_arm,
    change_to_guided,
    change_to_takeoff,
    change_to_return,
    change_to_land,
    change_to_loiter,
    change_armed,
    change_disarmed,
    connect,
    disconnect,
)

urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
    path("dynamic_time/", dynamic_time, name="dynamic_time"),
    path("get_mode/", get_mode, name="get_mode"),
    path("get_coordinates/", get_coordinates, name="get_coordinates"),
    path("get_ready_to_arm/", get_ready_to_arm, name="get_ready_to_arm"),
    path("change_to_guided/", change_to_guided, name="change_to_guided"),
    path("change_to_takeoff/", change_to_takeoff, name="change_to_takeoff"),
    path("change_to_return/", change_to_return, name="change_to_return"),
    path("change_to_land/", change_to_land, name="change_to_land"),
    path("change_to_loiter/", change_to_loiter, name="change_to_loiter"),
    path("change_armed/", change_armed, name="change_armed"),
    path("change_disarmed/", change_disarmed, name="change_disarmed"),
    path("disconnect/", disconnect, name="disconnect"),
    path("connect/", connect, name="connect"),
]
