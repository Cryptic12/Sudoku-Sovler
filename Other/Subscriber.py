
class Subscriber:
    __notifyFunc = None
    __subscriberId = None

    def __init__(self, notifyFunc):
        self.__notifyFunc = notifyFunc

    def notify(self, event):
        self.__notifyFunc(event)

    def setNotifyFunc(self, notifyFunc):
        self.__notifyFunc = notifyFunc

    def getNotifyFunc(self):
        return self.__notifyFunc

    def setId(self, id):
        self.__subscriberId = id

    def getId(self):
        return self.__subscriberId
