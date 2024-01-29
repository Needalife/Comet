import operator,os,pymongo, pandas as pd
from dotenv import load_dotenv

load_dotenv()
mongo_uri = os.getenv('mongo_uri')

class Calculator:
    def __init__(self,operator,x,y):
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

class Mongo:
    def __init__(self,uri=None):
        self.uri = mongo_uri
        self.client = pymongo.MongoClient(self.uri)
        self.database = ""
        
    def write(self,collection,database,username,userkey):
        self.database = self.client[f"{database}"]
        collection = self.database[f"{collection}"]
        
        user_dict = {"username": f"{username}", "key": f"{userkey}"}
        collection.insert_one(user_dict)
    
    def delete(self,collection,database,username):
        self.database = self.client[f"{database}"]
        collection = self.database[f"{collection}"]
        
        user_dict = {"username": f"{username}"}
        collection.delete_one(user_dict)

