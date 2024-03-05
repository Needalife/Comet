import os,pymongo,requests,datetime
from dotenv import load_dotenv
from datetime import timezone

load_dotenv()

class Converter:
    def __init__(self,expression=None):
        self.expression = expression
    
    def convert_operator(self):
        users_symbol = {
            'x':'*',
            '^':'**',
            ':':'/'}
        
        for key,value in users_symbol.items():
            if key in self.expression:
                self.expression = self.expression.replace(key,value)
        
        return self.expression
    
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

    @staticmethod
    def display_currency(copper):
        silver = copper // 100
        copper_remainder = copper % 100
        gold = silver // 100
        silver_remainder = silver % 100
        return gold, silver_remainder, copper_remainder

job = Converter("8^2")
job.convert_operator()
print(job.expression)

class Mongo:
    def __init__(self,database=None):
        self.uri = os.getenv('mongo_uri')
        self.client = pymongo.MongoClient(self.uri)
        self.database = database
        
    def write_user_api(self,collection,database,username,userkey):
        self.database = self.client[f"{database}"]
        collection = self.database[f"{collection}"]
        
        user_dict = {"user": f"{username}", "key": f"{userkey}"}
        collection.insert_one(user_dict)
    
    def delete_user_document(self,collection,database,username,filter_is=None,filter_content=None):
        self.database = self.client[f"{database}"]
        collection = self.database[f"{collection}"]
        
        if filter_is is None:
            user_dict = {"user": f"{username}"}
            collection.delete_one(user_dict)
        else:
            user_dict = {"user": f"{username}", f"{filter_is}" : f"{filter_content}"}
            collection.delete_one(user_dict)
            
    def read_user_api(self, collection, database, username):
        self.database = self.client[f"{database}"]
        collection = self.database[f"{collection}"]
        
        user_dict = {"user": f"{username}"}
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
    
        if mysticforge_data or items_recipe_data:
            return mysticforge_data, items_recipe_data
        else:
            return None
    
    def get_item_name(self, database, item_id):
        self.database = self.client[f"{database}"]
        collection = self.database["items_name"]
        
        query = {"item_id": f"{item_id}"}
        data = collection.find(query)
        
        for i in data: item_name = i["name"]
        
        return item_name
    
    def store_link(self,username,title,link):
        database = self.client[f"{self.database}"]
        collection = database['link']
        current_time = datetime.datetime.now(timezone.utc)
        utc_time = current_time.replace(tzinfo=timezone.utc)
        
        user_dict = {"user" : f"{username}", 
                     "title" : f"{title}", 
                     "link" : f"{link}", 
                     "timestamp" : f"{utc_time}"}
        
        collection.insert_one(user_dict)
    
    def get_links(self,username):
        database = self.client[f"{self.database}"]
        collection = database['link']
        query = {"user":f"{username}"}
        data = [i for i in collection.find(query)]
        return data

    def get_item_id(self, database, item_name):
        self.database = self.client[f"{database}"]
        collection = self.database["items_name"]
        
        query = {"name": f"{item_name}"}
        data = collection.find(query)
        
        for i in data: item_id = i["item_id"]
        
        return item_id
    
    @staticmethod
    def get_item_icon(item_name):
        job = Mongo()
        item_id = job.get_item_id("gw2_items",item_name)
        url = f'https://api.guildwars2.com/v2/items/{item_id}'
        
        response = requests.get(url)
        data = response.json()
        icon = data['icon']
        
        return icon
    
class EmbedCursor:
    def __init__(self,embed):
        self.embed = embed
    
    def add_row(self,col1,col2,col3,isHeader=False):
        if isHeader == True:
            self.embed.add_field(name=f"{col1}",value=" ", inline=True)
            self.embed.add_field(name=f"{col2}",value=" ", inline=True)
            self.embed.add_field(name=f"{col3}",value=" ", inline=True)
        else:
            self.embed.add_field(name="",value=f"{col1}", inline=True)
            self.embed.add_field(name="",value=f"{col2}", inline=True)
            self.embed.add_field(name="",value=f"{col3}", inline=True)

    def add_2_column_row(self,category,value):
        self.embed.add_field(name=f"{category}",value=" ", inline=True)
        self.embed.add_field(name="",value=f"{value}", inline=True)
        self.embed.add_field(name="",value=f" ", inline=True)

