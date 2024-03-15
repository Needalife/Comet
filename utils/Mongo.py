import os,pymongo,requests,datetime
from dotenv import load_dotenv
from datetime import timezone

load_dotenv()

class Mongo:
    def __init__(self,database=None):
        self.uri = os.getenv('mongo_uri')
        self.client = pymongo.MongoClient(self.uri)
        self.database = database
    
    def delete_user_document(self,collection,database,username,filter_is=None,filter_content=None):
        self.database = self.client[f"{database}"]
        collection = self.database[f"{collection}"]
        
        if filter_is is None:
            user_dict = {"user": f"{username}"}
            collection.delete_one(user_dict)
        else:
            user_dict = {"user": f"{username}", f"{filter_is}" : f"{filter_content}"}
            collection.delete_one(user_dict)
                
    def storeLink(self,username,title,link):
        database = self.client[f"{self.database}"]
        collection = database['link']
        current_time = datetime.datetime.now(timezone.utc)
        utc_time = current_time.replace(tzinfo=timezone.utc)
        
        user_dict = {"user" : f"{username}", 
                     "title" : f"{title}", 
                     "link" : f"{link}", 
                     "timestamp" : f"{utc_time}"}
        
        collection.insert_one(user_dict)

    def getLinks(self,username):
        database = self.client[f"{self.database}"]
        collection = database['link']
        query = {"user":f"{username}"}
        data = [i for i in collection.find(query)]
        
        return data
    
    def getAllDatabase(self):
        db = self.client.list_database_names()
        #get all non-system datbases!
        return [i for i in db if i not in ['local','admin']]
    
    def getAllCollection(self,database):
        database = self.client[f"{database}"]
        filter = {"name": {"$regex": r"^(?!system\.)"}}
        return database.list_collection_names(filter=filter)
    
    def getSize(self,database,collections:list):
        db = self.client[f"{database}"]
        colSize = [db.command("collstats",collection)['size'] for collection in collections] 
        col = [i for i in collections]
        
        return {k:v for (k,v) in zip(col,colSize)}

class gw2Items(Mongo):
    def __init__(self, database=None):
        super().__init__(database)
        self.key = ''
        self.database = self.client[f"{database}"] 
        if database == "api-key":
            #user api key
            self.collection = self.database["gw2"]
        
    def write_user_api(self,username,userkey):
        user_dict = {"user": f"{username}", "key": f"{userkey}"}
        self.collection.insert_one(user_dict)

    def delete_user_api(self,username):
        user_dict = {"user": f"{username}"}
        self.collection.delete_one(user_dict)
    
    def read_user_api(self, username):
        user_dict = {"user": f"{username}"}
        return self.collection.find(user_dict)
    
    def get_user_info(self, username):
        data = self.read_user_api(username)
        for value in data: self.key = value['key']
        
        gw2_endpoint = 'https://api.guildwars2.com/v2/account'
        headers = {'Authorization': f'Bearer {self.key}'}
        response = requests.get(gw2_endpoint, headers=headers)
        
        if response.status_code == 200:
            account_data = response.json()
            return account_data['name'],account_data['age'],account_data['fractal_level'],account_data['wvw_rank']
        else:
            return None
    
    #this method can only be call when get_user_info is already used!
    def get_user_leggy(self):
        leggy_url = 'https://api.guildwars2.com/v2/account/legendaryarmory'
        headers = {'Authorization': f'Bearer {self.key}'}
        
        response = requests.get(leggy_url, headers=headers)
        leggys_data = response.json()
        
        return leggys_data
        
    def get_item_name(self,item_id):
        item_dict = {"item_id": f"{item_id}"}
        collection = self.database['items_name']
        
        for i in collection.find(item_dict): item_name = i['name']
        return item_name

    def get_item_recipe(self,item_name):
        name_collection = self.database["items_name"]
        mysticforge_recipe_collection = self.database["mysticforge_recipe"]
        items_recipe_collection = self.database["items_recipe"]
        
        name_dict = {"name": f"{item_name}"}
        name_data = name_collection.find(name_dict)
        
        name_id = None
        for i in name_data: name_id = i["item_id"]
        
        query_id = {"output_item_id": int(name_id)}
        mysticforge_data = list(mysticforge_recipe_collection.find(query_id))
        items_recipe_data = list(items_recipe_collection.find(query_id))
    
        if mysticforge_data or items_recipe_data:
            return mysticforge_data, items_recipe_data
        else:
            return None

    def get_item_id(self,item_name):
        collection = self.database["items_name"]
        
        query = {"name": f"{item_name}"}
        data = collection.find(query)
        
        for i in data: item_id = i["item_id"]
        
        return item_id

    def get_item_icon(self,item_name):
        item_id = self.get_item_id(item_name)
        url = f'https://api.guildwars2.com/v2/items/{item_id}'
        
        response = requests.get(url)
        data = response.json()
        icon = data['icon']
        
        return icon