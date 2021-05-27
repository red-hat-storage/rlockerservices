from queue_service import rlocker


by_data_label = lambda q: q.data.get('label')
by_data_name = lambda q: q.data.get('name')

by_data_label_and_priority = lambda q: (q.data.get('label'), q.priority, q.id)
by_data_name_and_priority = lambda q: (q.data.get('name'), q.priority, q.id)