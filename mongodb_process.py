from pymongo import MongoClient

class DBProcessor:
    def __init__(self):
        #mongoDB connection
        self.client = MongoClient('mongodb://adminUser:adminPassword@54.177.184.253:27017/')
        self.db = self.client['smartcity']
        self.drone_collection = self.db['drone']

        #sql connection

    # get
    def get_drone_info(self, drone_id):
       drone_info = self.drone_collection.find_one({'drone_id': drone_id})
        