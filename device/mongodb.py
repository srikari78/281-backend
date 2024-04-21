from pymongo import MongoClient
from django.utils import timezone

class MongoDBProcessor:
    def __init__(self):
        #mongoDB connection
        self.client = MongoClient('mongodb://adminUser:adminPassword@54.177.184.253:27017/')
        self.db = self.client['smartcity']
        self.drone_collection = self.db['drone']

    # get device info   
    def get_drone_info(self, drone_id):
        drone_info = self.drone_collection.find_one({'drone_id' : drone_id})
        print(drone_id, drone_info)
        if drone_info is not None:
            latitude = drone_info['latitude']
            longitude = drone_info['longitude']
            altitude = drone_info['altitude']
            district_id = drone_info['district_id']
            timestamp = str(timezone.now())
            
            """ else: 
            latitude = 10
            longitude = 10
            altitude =10
            district_id = 1
            timestamp = "10/5/23 4:47"
            """
        
        

        return {'drone_id': drone_id, 'latitude': latitude, 'longitude': longitude, 'altitude': altitude,  'timestamp':timestamp ,'district_id': district_id}

    #def get_image_url(self, index):
     #   drone_info = self.drone_collection.find_one({'cctv.index': index})
      #  image_url = drone_info['cctv']['imageData']['static']['currentImageURL']
       # return image_url
    
    