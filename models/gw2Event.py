#Todo
class gw2Event:
    def __init__(self,expansion,zone,name,waypoint,start,end,interval,isCore=False,metaType=None):
        self.expansion = expansion
        self.zone = zone
        self.name = name
        self.waypoint = waypoint
        self.start = start
        self.end = end
        self.interval = interval
        if isCore == True:
            self.metaType = metaType
        
    