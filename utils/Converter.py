import math,pytz
from datetime import datetime

class Converter:
    def __init__(self,expression=None):
        self.expression = expression
    
    @staticmethod
    def replace_key_with_value(dictionary,expression):
        for key,value in dictionary.items():
            if key in expression:
                expression = expression.replace(key,value)
            
        return expression
    
    def convert(self):
        user_symbols = {
            'x': '*',
            '^': '**',
            ':': '/',
            'sin': 'math.sin',
            'cos': 'math.cos',
            'tan': 'math.tan',
            'pi': 'math.pi'
        }
        
        self.expression = Converter.replace_key_with_value(user_symbols, self.expression)    

    def final(self):
        self.convert()
        return self.expression
    
    @staticmethod
    def displayTime(seconds, granularity=2):
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
    def displayCurrency(copper):
        silver = copper // 100
        copper_remainder = copper % 100
        gold = silver // 100
        silver_remainder = silver % 100
        return gold, silver_remainder, copper_remainder
    
    @staticmethod
    def displayBytes(byteSize):
        if byteSize == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(byteSize, 1024)))
        p = math.pow(1024, i)
        s = round(byteSize / p, 2)
        return "%s %s" % (s, size_name[i])
    
    @staticmethod
    def timeVN(time):
        return time.astimezone(pytz.timezone('Asia/Ho_Chi_Minh')).strftime("%H:%M")
