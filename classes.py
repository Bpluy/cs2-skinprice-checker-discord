class User:
    dictSkins: dict
    
    def __init__(self):
        self.dictSkins = dict()

    def addSkin(self, skin, price):
        if (self.dictSkins.get(skin)) == None:
            self.dictSkins[skin] = price
    
    