
# Singleton Location Class
class MyLocation(object):
    class __OnlyOne:
        def __init__(self):
            self.latitude = 0.0
            self.longitude = 0.0
        def __str__(self):
            return repr(self)
    instance = None
    def __new__(cls): # __new__ always a classmethod
        if not MyLocation.instance:
            MyLocation.instance = MyLocation.__OnlyOne()
        return MyLocation.instance
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __setattr__(self, name):
        return setattr(self.instance, name)
