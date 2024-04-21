from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('addDevice', views.addDevice),
    path('UpdateDevice', views.UpdateDeviceInfo),
    path('GetDevice', views.getDeviceInfo),
    path('DeleteDevice', views.deleteDevice),
    path('DisableDevice/', views.disableDevice),
    path('GetDeviceOfDistrict/', views.get_device_of_district_id),
]