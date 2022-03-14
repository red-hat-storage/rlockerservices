import os
import resource_sync_service.constants as const
from service_base.service_base import ServiceBase
from service_base.connection import ResourceLockerConnection

rlocker = ResourceLockerConnection()


class ResourceSyncService(ServiceBase):
    def __init__(self):
        print("init")

    def run(self):
        print("Yess")

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Yess")

    @staticmethod
    def run_prerequisites():
        print('Prerequisites')