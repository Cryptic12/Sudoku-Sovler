
class Subscriber:
    _notify_func = None
    _subscriber_id = None

    def __init__(self, notify_func):
        self._notify_func = notify_func

    def notify(self, event):
        self._notify_func(event)

    def set_notify_func(self, _notify_func):
        self._notify_func = _notify_func

    def get_notify_func(self):
        return self._notify_func

    def set_id(self, id):
        self._subscriber_id = id

    def get_id(self):
        return self._subscriber_id
