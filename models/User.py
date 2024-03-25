class User:
    def __init__(self,username,created_at,user_id,display_avatar,description = None):
        self.username = username
        self.user_id = user_id
        self.created_at = created_at
        self.display_avatar = display_avatar
        self.description = description
    
    def userDocument(self):
        
        data = {
            'name' : f"{self.username}",
            'user_id' : f"{self.user_id}",
            'display_avatar' : f"{self.display_avatar}",
            'description' : f"{self.description}",
            'created_at' : f"{self.created_at}",
        }
        
        return data