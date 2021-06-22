# Resource Locker Services project
## This project includes the services for [rlocker](https://github.com/jimdevops19/rlocker).

### Project Dependencies:
 - [rlocker](https://github.com/jimdevops19/rlocker) - The Django platform both with REST API endpoints and web UI
 - [rlockertools](https://github.com/jimdevops19/rlockertools) -  A Python based client interface to interact with the platform
 

### Quick Start Video will be added soon

Project Architecture:

Each directory represents a Python Package, that is being used as an independent service
 - __service_base:__ The base package, we will use this to inherit from it for each service (Python package) that we want to create
   - [__ init __.py](service_base/__init__.py): Packaging this service_base dir
   - [constants.py](service_base/constants.py): Constants for the package
   - [service_base.py](service_base/service_base.py): The main class of the package, to define methods

 - __queue_service:__ Service to handle the queues that are on PENDING state on [rlocker](https://github.com/jimdevops19/rlocker)
   - [__ init __.py](queue_service/__init__.py): Packaging this queue_service dir. We load the configurations in this __ __init__ __ file.
   - [constants.py](queue_service/constants.py): Constants for the package
   - [defaultconf.yaml](queue_service/defaultconf.yaml): Default configurations of the svc. This will be used if some of them are NOT passed as ENV variable.
   - [queue_service.py](queue_service/queue_service.py): The file with the class to define methods, as well as what the svc will do when it is called from [run.py](run.py)
   - [rqueue.py](queue_service/rqueue.py): A Python class to objectify the resources that are grabbed from API calls.
   - [utils.py](queue_service/utils.py): Helping function for specific actions like time calculations.
