import time
import sys
import queue_service.constants as const
import os
import pprint as pp
from service_base.service_base import ServiceBase
from queue_service import rlocker, conf
from queue_service.rqueue import Rqueue


class QueueService(ServiceBase):
    def __init__(self):
        self.initializing_queues = rlocker.get_queues(status=const.STATUS_INITIALIZING)
        # We should fill this right after we checked what queues are not put in status pending
        self.pending_queues = None

    def run(self):
        """
        Actions to run when the service gets initialized
        :return None:
        """
        self.put_queues_on_pending()
        self.pending_queues = rlocker.get_queues(status=const.STATUS_PENDING)
        self.instantiate_pending_queue_objects()
        Rqueue.group_all()
        pp.pprint(Rqueue.grouped_queues)
        for group in Rqueue.grouped_queues:
            if group.get("group_type") == "label":
                resources = rlocker.get_lockable_resources(
                    free_only=True, label_matches=group.get("group_name")
                )
            elif group.get("group_type") == "name":
                resources = rlocker.get_lockable_resources(
                    free_only=True, name=group.get("group_name")
                )
            else:
                raise Exception("Group type should be either name or label!")

            if not resources == []:
                group_queues = group.get("queues")
                next_queue = group_queues.pop(0)
                next_resource = resources.pop(0)

                attempt_lock = rlocker.lock_resource(
                    next_resource,
                    signoff=next_queue.data.get("signoff"),
                    link=next_queue.data.get("link"),
                )
                print(attempt_lock.json())

                # If attempt to lock was successful:
                if attempt_lock.json().get("is_locked"):
                    # TODO: It might be better idea to display the final locked resource as an addition to queue's data JSON FIELD, currently we add to the description
                    rlocker.change_queue(
                        next_queue.id,
                        status=const.STATUS_FINISHED,
                        description=f"Final Resource:{next_resource.get('name')}",
                    )
                else:
                    rlocker.change_queue(
                        next_queue.id,
                        status=const.STATUS_FAILED,
                        description=attempt_lock.text[:2048],
                    )

        return None

    def put_queues_on_pending(self):
        """
        This is a method that needs to be started with the startup of the svc.
        Reason: When the service starts, it needs to grab all the INITIALIZING queues,
            and put them on pending state.
        This will we a sign that this svc is healthy, and also it is being handled.
        :return: None
        """
        for queue in self.initializing_queues:
            queue_id = queue.get("id")
            queue_response = rlocker.change_queue(queue_id, status="PENDING")
            # For each queue, we should verify that the queues changed to being PENDING:
            is_queue_changed = (
                dict(queue_response.json()).get("status") == const.STATUS_PENDING
            )
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
                if len(self.initializing_queues) > 0
                else f"No queues to Initialize. \n"
            )
            print(
                f"Total Queues that are {const.STATUS_PENDING}: "
                f"{len(rlocker.get_queues(status=const.STATUS_PENDING))}"
            )

        return None

    def instantiate_pending_queue_objects(self):
        """
        A method to instantiate objects so it will be easier
            to manipulate and filter specific data with the pending queues.
        We do not want to send requests, once we have the necessary info
            from get_queues()
        :return None:
        """
        for queue in self.pending_queues:
            # We want to initialize an instance of Rqueue only in case it is not already exists
            # as Rqueue instance:
            Rqueue(
                id=queue.get("id"),
                priority=queue.get("priority"),
                data=queue.get("data"),
            )

        return None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        We use context manager to describe what the service should to as post
            actions, after each beat.

        Actions:
             - Sleep the program to rest few seconds before next beat
             - Use clean console screen in order to display the most updated
                  status of all queues.
             - Clear the variables content that are indexed each beat, so that we
                will not have duplicated data on those variables

        Handling Exception parameters that we need to receive:
        :param exc_type:
        :param exc_val:
        :param exc_tb:

        :return: None
        """

        time.sleep(conf["svc"].get("INTERVAL"))
        os.system("cls") if os.name == "nt" else os.system("clear")
        Rqueue.all.clear()
        Rqueue.grouped_queues.clear()
