import json
from queue_service.utils import group_has_label

class Rqueue:
    all = []

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.priority = kwargs.get('priority')
        self.data = json.loads(kwargs.get('data'))

        # Keep this line last, we want to store all the instances
            # after the init actions in a list
        Rqueue.all.append(self)

    def __repr__(self):
        '''
        Decide the representation of each instance

        :return: string of representation
        '''
        return f'Rqueue({self.id}, {self.priority}, {self.data})'

    @property
    def has_associated_resource(self):
        '''
        Method uses this as an indication to check if the queue is with an
            associated lockable resource.
        If ID or the lockable resource exists, then it means that the lock request was
            made for a specific id.
        If there is no ID, it means that the request looks for one among multiple
            lockable resources.
        :return bool:
        '''
        queue_data_id = self.data.get('id')
        return queue_data_id is not None

    @property
    def has_not_associated_resource(self):
        '''
        Method uses this as an indication to check if the queue is without an
            associated lockable resource
        If ID or the lockable resource exists, then it means that the lock request was
            made for a specific id.
        If there is no ID, it means that the request looks for one among multiple
            lockable resources.

        :return bool:
        '''
        queue_data_id = self.data.get('id')
        return queue_data_id is None

    @staticmethod
    def associated_resource_rqueues():
        '''
        Gets all the resources with an associated resource
        :return: List:
        '''
        rqueues_list = []
        for rqueue in Rqueue.all:
            if rqueue.has_associated_resource:
                rqueues_list.append(rqueue)

        return rqueues_list

    @staticmethod
    def non_associated_resource_rqueues():
        '''
        Gets all the resources without an associated resource
            And it's with a label
        :return: List:
        '''
        rqueues_list = []
        for rqueue in Rqueue.all:
            if rqueue.has_not_associated_resource:
                rqueues_list.append(rqueue)

        return rqueues_list

    @staticmethod
    def group_all():
        '''
        Grouping the queues by their search up lockable resource.
        For example: Two or more queues that are interested to have a resource
            with the same label, should be in the same group.
        OR:
        Two or more queues that are interested to lock the resource with
            the same ID (or resource name), should be in the same group as well.
        :return:
        '''
        group = []


        return group


