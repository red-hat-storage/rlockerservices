import pprint as pp
import time
from rlockertools.resourcelocker import ResourceLocker


rlocker = ResourceLocker(
    instance_url='http://127.0.0.1:8000',
    token='8148bb8ffd6ffbc335947885eb2f3dff8c181e8f'
)

while True:
    c = rlocker.get_queues(status='PENDING')
    print(len(c))
    pp.pprint(c)

    time.sleep(2)