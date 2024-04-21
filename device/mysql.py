from .models import Device

class MysqlProcessor:
    def __init__(self):
        pass

    def add_device(self, device_info):
        if Device.objects.filter(drone_id=device_info['drone_id']).exists():
            return False
        else:
            device_mysql = Device(drone_id=device_info['drone_id'], latitude=device_info['latitude'], longitude=device_info['longitude'], altitude=device_info['altitude'], timestamp=device_info['timestamp'], district_id=device_info['district_id'])
            device_mysql.save()

    def update_device_info(self, device_info):
        if Device.objects.filter(drone_id=device_info['drone_id']).exists():
            device_mysql = Device.objects.get(drone_id=device_info['drone_id'])
            device_mysql.latitude = device_info['latitude']
            device_mysql.longitude = device_info['longitude']
            device_mysql.altitude = device_info['altitude']       
            device_mysql.district_id = device_info['district_id']
            device_mysql.timestamp = device_info['timestamp']
            device_mysql.save()
        else:
            device_mysql = Device(drone_id=device_info['drone_id'], latitude=device_info['latitude'], longitude=device_info['longitude'], altitude=device_info['altitude'], timestamp=device_info['timestamp'], district_id=device_info['district_id'])
            device_mysql.save()

    def get_device_info(self, request_drone_id):
        if Device.objects.filter(drone_id=request_drone_id).exists():
            device_mysql = Device.objects.get(drone_id=request_drone_id)
            device_info = {
                'latitude': device_mysql.latitude,
                'longitude': device_mysql.longitude,
                'altitude': device_mysql.altitude,
                'district_id': device_mysql.district_id,
                'timestamp': device_mysql.timestamp
            }
            return device_info
        else:
            return None
        
    def delete_device(self, request_drone_id):
        if Device.objects.filter(drone_id=request_drone_id).exists():
            device_mysql = Device.objects.get(drone_id=request_drone_id)
            device_mysql.delete()
            return True
        else:
            return False
    
    def updateImage(self, request_drone_id, image_url):
        if Device.objects.filter(drone_id=request_drone_id).exists():
            device_mysql = Device.objects.get(drone_id=request_drone_id)
            device_mysql.image_url = image_url
            device_mysql.save()
            return True
        else:
            return False
    
    def disable_device(self, request_drone_id):
        if Device.objects.filter(drone_id=request_drone_id).exists():
            device_mysql = Device.objects.get(drone_id=request_drone_id)
            device_mysql.enabled = False
            device_mysql.save()
            return True
        else:
            return False
    
    def get_all_devices_of_district(self, district):
        devices = Device.objects.filter(district=district)
        device_info = []
        for device in devices:
            device_info.append({
                'latitude': device.latitude,
                'longitude': device.longitude,
                'altitude': device.altitude,
                'district_id': device.district_id,
                'timestamp': device.timestamp
            })
        return device_info
    