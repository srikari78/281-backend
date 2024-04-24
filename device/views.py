from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponseNotAllowed, JsonResponse
from .mongodb import MongoDBProcessor
from .mysql import MysqlProcessor
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Device

import json


@csrf_exempt
def addDevice(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        altitude = data.get('altitude')
        timestamp = data.get('timestamp')
        dist_id = data.get('dist_id')
        status = data.get('status')
        if Device.objects.filter(id=id).exists():
            print("device already exists")
            return HttpResponse(json.dumps('device address already exist'), status=409)
        else:
            new_device = Device(id=id, latitude=latitude, longitude=longitude, altitude=altitude, timestamp=timestamp, dist_id=dist_id, status = status)
            new_device.save()
            print('device added')
            return HttpResponse(json.dumps('device succeed'), status=200)
    else:
        return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def UpdateDeviceInfo(request):
        if request.method == 'PUT':
            data = json.loads(request.body)
            id = data.get('update_id')
            latitude = data.get('update_latitude')
            longitude = data.get('update_longitude')
            altitude = data.get('update_altitude')
            timestamp = data.get('update_timestamp')
            dist_id = data.get('update_dist_id')
            status = data.get('update_status')

            try:
                device = Device.objects.get(id=id)
                device.latitude = latitude
                device.longitude = longitude
                device.altitude = altitude
                device.timestamp = timestamp
                device.dist_id = dist_id
                device.status = status
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
        id = data.get('id')
        try:
            device = Device.objects.get(id=id)
            device_data = {
                'id': device.id,
                'latitude': device.latitude,
                'longitude': device.longitude,
                'altitude': device.altitude,
                'timestamp': device.timestamp,
                'dist_id': device.dist_id,
                'status': device.status
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
        id = data.get('id')
        if id is None:
            return HttpResponse('Drone ID not provided', status=400)

        try:
            device = Device.objects.get(id=id)
            device.delete()
            print('device deleted')
            return HttpResponse('Device deleted', status=200)
        except Device.DoesNotExist:
            return HttpResponse('Device not found', status=404)
    else:
        return HttpResponseNotAllowed(['DELETE'])
    
@csrf_exempt 
def get_video_urls(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')
        print("Received id:", id)
        mongodb = MongoDBProcessor()
        try:
            deviceInfo = mongodb.get_drone_info(id)
            device_data = {
                'id': id,
                'videourl' : deviceInfo['video_url']
            }
            print(device_data)
            return JsonResponse(device_data)
        except Device.DoesNotExist:
            return JsonResponse({'error': 'video url not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    

@csrf_exempt 
def getAllDevices(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        id = data.get('id')
        try:
            device = Device.objects.get(id=id)
            device_data = {
                'id': device.id,
                'latitude': device.latitude,
                'longitude': device.longitude,
                'altitude': device.altitude,
                'timestamp': device.timestamp,
                'dist_id': device.dist_id,
                'video_url': device.video_url,
                'status':device.status
            }
            return JsonResponse(device_data)
        except Device.DoesNotExist:
            return JsonResponse({'error': 'Device not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
        
def updateImage(request):
    id = "1"
    # update image url
    mongodb = MongoDBProcessor()
    image_url = mongodb.get_image_url(id)
    db = MysqlProcessor()
    if db.updateImage(id, image_url):
        return HttpResponse('Image updated')
    else:
        return HttpResponse('Device not found')

def disableDevice(request):
    id = "1"
    # disable device
    db = MysqlProcessor()
    if db.disable_device(id):
        return HttpResponse('Device disabled')
    else:
        return HttpResponse('Device not found')