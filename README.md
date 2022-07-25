# Resource Locker Services project
## This project includes the services for [rlocker](https://github.com/red-hat-storage/rlocker).

### Project Dependencies:
 - [rlocker](https://github.com/red-hat-storage/rlocker) - The Django platform both with REST API endpoints and web UI
 - [rlockertools](https://github.com/red-hat-storage/rlockertools) -  A Python based client interface to interact with the platform
 

### Quick Start Video will be added soon

Project Architecture:

Each directory represents a Python Package, that is being used as an independent service
 - __service_base:__ The base package, we will use this to inherit from it for each service (Python package) that we want to create
   - [__ init __.py](service_base/__init__.py): Packaging this service_base dir
   - [constants.py](service_base/constants.py): Constants for the package
   - [connection.py](service_base/connection.py): Module related to connection to the Resource Locker instance
   - [service_base.py](service_base/service_base.py): The main class of the package, to define methods

 - __queue_service:__ Service to handle the queues that are on PENDING state on [rlocker](https://github.com/red-hat-storage/rlocker)
   - [health](queue_service/health): A python package that checks the health of the svc. Useful for automatic restarting when used with `livenessProbe` section in production.
   - [__ init __.py](queue_service/__init__.py): Packaging this queue_service dir. We load the configurations in this __ __init__ __ file.
   - [constants.py](queue_service/constants.py): Constants for the package
   - [defaultconf.yaml](queue_service/defaultconf.yaml): Default configurations of the svc. This will be used if some of them are NOT passed as ENV variable.
   - [queue_service.py](queue_service/queue_service.py): The file with the class to define methods, as well as what the svc will do when it is called from [run.py](run.py)
   - [rqueue.py](queue_service/rqueue.py): A Python class to objectify the resources that are grabbed from API calls.
   - [utils.py](queue_service/utils.py): Helping function for specific actions like time calculations.


## Dev mode:
 - The following are commands to run in your terminal, each line represents a pattern of:   `command to run` __Explanation__
   - `git clone https://github.com/red-hat-storage/rlockerservices.git` __Clones the project__
   - `cd rlockerservices` __Change directory__
   - `python --version` __Python3.8 is required! (Python3.9 not tested, Python3.10 not supported)__
   - `python -m venv venv` __Create a virtual environment for this Python service__ (Note: Use python3.8 instead if your default python is something else)
   - The following command differs from Windows to Linux systems:
     - `venv\Scripts\activate` __Run this to activate the venv on Windows__
     - `source venv/bin/activate` __Run this to activate the venv on Linux__
   - `pip install -r requirements.txt` __Install the required packages__
 - The following commands are environment variable setups. The command to set an env variable is `export` __(PLEASE USE SET AND NOT EXPORT IN WINDOWS!)__
   - Visit the Resource Locker instance you are running, __be sure that you are logged in to the Resource Locker__
     - Click the dropdown in the top navigation bar, near your logged-in username, select `Copy API Token`. Your users API token should be copied to the clipboard (Could be pasted the next time you send a Ctrl+V) 
     - `export RESOURCE_LOCKER_TOKEN='<YOUR_COPIED_TOKEN>'` Set this env variable. The wrapping with single quotes is important!
     - `export RESOURCE_LOCKER_URL='<YOUR_URL_OF_RESOURCE_LOCKER>'` Set this env variable. The wrapping with single quotes is important! (for i.e: http://127.0.0.1:8000)
 - Launch the queue_service
   - `python run.py --svc-kind queue_service`
 - Next Steps:
   - Visit the [rlockertools](https://github.com/red-hat-storage/rlockertools) project in order to ask for lockable resources automatically from the rlocker-cli. 
