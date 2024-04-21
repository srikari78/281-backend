from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponseNotAllowed
from .mongodb import MongoDBProcessor
from .mysql import MysqlProcessor
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Device


import json


"""def addDevice(request):
    drone_id = "5"
     # add device info
    mongodb = MongoDBProcessor()
    mysql = MysqlProcessor()
    #print(drone_id)
    deviceInfo = mongodb.get_drone_info(drone_id)
    #print(drone_id)
    print(deviceInfo)
    
    #mysql.add_device(deviceInfo)
    #return HttpResponse('Device added')

    if mysql.add_device(deviceInfo):      
       return HttpResponse('Device added')
    else:
        return HttpResponse('Device already exists')
        #return HttpResponse(json.dumps(deviceInfo))
    """
@csrf_exempt

def addDevice(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        drone_id = data.get('drone_id')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        altitude = data.get('altitude')
        timestamp = data.get('timestamp')
        district_id = data.get('district_id')
        print(data)

        if Device.objects.filter(drone_id=drone_id).exists():
            print("device already exists")
            return HttpResponse(json.dumps('device address already exist'), status=409)
        else:
            new_device = Device(drone_id=drone_id, latitude=latitude, longitude=longitude, altitude=altitude, timestamp=timestamp, district_id=district_id)
            new_device.save()
            print('device added')
            return HttpResponse(json.dumps('device succeed'), status=200)
    else:
        return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def UpdateDeviceInfo(request):
        if request.method == 'PUT':
            data = json.loads(request.body)
            drone_id = data.get('update_drone_id')
            latitude = data.get('update_latitude')
            longitude = data.get('update_longitude')
            altitude = data.get('update_altitude')
            timestamp = data.get('update_timestamp')
            district_id = data.get('update_district_id')

            try:
                device = Device.objects.get(drone_id=drone_id)
                device.latitude = latitude
                device.longitude = longitude
                device.altitude = altitude
                device.timestamp = timestamp
                device.district_id = district_id
                device.save()
                print('Device updated successfully')
                return HttpResponse(json.dumps('Device updated successfully'), status=200)
            except Device.DoesNotExist:
                print("Device does not exist")
                return HttpResponse(json.dumps('Device does not exist'), status=404)
        else:
            return HttpResponseNotAllowed(['PUT'])
@csrf_exempt
def getDeviceInfo(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        drone_id = data.get('drone_id')
        try:
            device = Device.objects.get(drone_id=drone_id)
            device_data = {
                'drone_id': device.drone_id,
                'latitude': device.latitude,
                'longitude': device.longitude,
                'altitude': device.altitude,
                'timestamp': device.timestamp,
                'district_id': device.district_id
            }
            return JsonResponse(device_data)
        except Device.DoesNotExist:
            return JsonResponse({'error': 'Device not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def deleteDevice(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        drone_id = data.get('drone_id')
        if drone_id is None:
            return HttpResponse('Drone ID not provided', status=400)

        try:
            device = Device.objects.get(drone_id=drone_id)
            device.delete()
            print('device deleted')
            return HttpResponse('Device deleted', status=200)
        except Device.DoesNotExist:
            return HttpResponse('Device not found', status=404)
    else:
        return HttpResponseNotAllowed(['DELETE'])

def updateImage(request):
    drone_id = "1"
    # update image url
    mongodb = MongoDBProcessor()
    image_url = mongodb.get_image_url(drone_id)
    db = MysqlProcessor()
    if db.updateImage(drone_id, image_url):
        return HttpResponse('Image updated')
    else:
        return HttpResponse('Device not found')

def disableDevice(request):
    drone_id = "1"
    # disable device
    db = MysqlProcessor()
    if db.disable_device(drone_id):
        return HttpResponse('Device disabled')
    else:
        return HttpResponse('Device not found')

def get_device_of_district_id(request):
    district_id = "1"
    # get device info of district
    db = MysqlProcessor()
    devices = db.get_all_devices_of_district_id(district_id)
    print(devices)
    return HttpResponse(devices)