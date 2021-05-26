import time
import sys
import queue_service.constants as const
from service_base.service_base import ServiceBase
from queue_service import rlocker
from queue_service.rqueue import Rqueue

class QueueService(ServiceBase):
    def __init__(self):
        self.all_queues = rlocker.get_queues()

    def run(self):
        '''
        Actions to run when the service gets initialized
        :return:
        '''
        self.put_queues_on_pending()
        self.instantiate_objects()
        for i in Rqueue.group_all():
            print(i)

    def put_queues_on_pending(self):
        '''
        This is a method that needs to be started with the startup of the svc.
        Reason: When the service starts, it needs to grab all the INITIALIZING queues,
            and put them on pending state.
        This will we a sign that this svc is healthy, and also it is being handled.
        :return: None
        '''
        for queue in self.all_queues:
            queue_id = queue.get('id')
            queue_response = rlocker.change_queue(queue_id, status='PENDING')
            # For each queue, we should verify that the queues changed to being PENDING:
            is_queue_changed = dict(queue_response.json()).get('status') == const.STATUS_PENDING
            if not is_queue_changed:
                print(
                    f"There was a problem changing queue with ID {queue_id} to {const.STATUS_PENDING}! \n"
                    f"Unrecoverable error. Service Exiting..."
                )
                sys.exit()

        else:
            # All the checks did not enter if not is_queue_changed.
            # Therefore, service is ready to keep running.
            print(
                f"Service put all queues on {const.STATUS_PENDING} successfully! \n"
                f"Total Services that are {const.STATUS_PENDING}: {len(self.all_queues)}"
            )

    def instantiate_objects(self):
        '''
        A method to instantiate objects so it will be easier
            to manipulate and filter specific data.
        We do not want to send requests, once we have the necessary info
            from get_queues()
        :return None:
        '''
        for queue in self.all_queues:
            Rqueue(
                id=queue.get('id'),
                priority=queue.get('priority'),
                data=queue.get('data')
            )
        return None


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        time.sleep(120)
