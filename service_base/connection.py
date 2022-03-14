import os
from queue_service import conf
from rlockertools.resourcelocker import ResourceLocker


class Singleton(type):
    _instances = {}

    # Each of the following functions use cls instead of self
    # to emphasize that although they are instance methods of
    # Singleton, they are also *class* methods of a class defined
    # with Singleton
    # Implementation:
    # SO Poll: https://stackoverflow.com/questions/50065276/clearing-a-metaclass-singleton/50065732#50065732
    def __call__(cls, *args, **kwargs):
        if cls not in Singleton._instances:
            Singleton._instances[cls] = super().__call__(*args, **kwargs)
        return Singleton._instances[cls]

    def clear(cls):
        try:
            del Singleton._instances[cls]
        except KeyError:
            pass


class ResourceLockerConnection(ResourceLocker, metaclass=Singleton):
    # Resource Locker library will be instantiated against the provided environment variable
    # that will be injected once the container starts.
    # If it is None, it will try to use the one that is provided from the defaultconf.yaml file
    def __init__(self):
        super(ResourceLockerConnection, self).__init__(
            instance_url=os.environ.get("RESOURCE_LOCKER_URL")
            or conf["svc"].get("RESOURCE_LOCKER_URL"),
            token=os.environ.get("RESOURCE_LOCKER_TOKEN")
            or conf["svc"].get("RESOURCE_LOCKER_TOKEN"),
        )
