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