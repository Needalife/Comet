import operator,os,pymongo, pandas as pd, json
from dotenv import load_dotenv

load_dotenv()

class Calculator:
    def __init__(self,operator=None,x=None,y=None):
        self.operator = operator
        self.x = x
        self.y = y

    def calculation(self):
        op_dict = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}
        if self.operator in op_dict.keys():
            for key in op_dict:
                if self.operator == key:
                    result = op_dict[f"{key}"](self.x,self.y)
                    return result
        else:
            return "Invalid operator"
        
    @staticmethod
    def display_time(seconds, granularity=2):
        intervals = (
            ('weeks', 604800),  
            ('days', 86400),    
            ('hours', 3600),    
            ('seconds', 1),
        )
        result = []

        for name, count in intervals:
            value = seconds // count
            if value:
                seconds -= value * count
                if value == 1:
                    name = name.rstrip('s')
                result.append("{} {}".format(value, name))
        return ', '.join(result[:granularity])

class Mongo:
    def __init__(self,uri=None,database=None):
        self.uri = os.getenv('mongo_uri')
        self.client = pymongo.MongoClient(self.uri)
        self.database = database
        
    def write_user_api(self,collection,database,username,userkey):
        self.database = self.client[f"{database}"]
        collection = self.database[f"{collection}"]
        
        user_dict = {"username": f"{username}", "key": f"{userkey}"}
        collection.insert_one(user_dict)
    
    def delete_user_api(self,collection,database,username):
        self.database = self.client[f"{database}"]
        collection = self.database[f"{collection}"]
        
        user_dict = {"username": f"{username}"}
        collection.delete_one(user_dict)
    
    def read_user_api(self, collection, database, username):
        self.database = self.client[f"{database}"]
        collection = self.database[f"{collection}"]
        
        user_dict = {"username": f"{username}"}
        return collection.find(user_dict)

    def get_recipe(self,database,item_name):
        self.database = self.client[f"{database}"]
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
    
        if mysticforge_data and items_recipe_data:
            return mysticforge_data, items_recipe_data
        elif mysticforge_data:
            return mysticforge_data
        elif items_recipe_data:
            return items_recipe_data
        else:
            return None
    
    def get_item_name(self, database, item_id):
        self.database = self.client[f"{database}"]
        collection = self.database["items_name"]
        
        query = {"item_id": f"{item_id}"}
        data = collection.find(query)
        
        for i in data: item_name = i["name"]
        
        return item_name
        
job = Mongo()
print(job.get_item_name("gw2_items",4))
        
        
        
        
        