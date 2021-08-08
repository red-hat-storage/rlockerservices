# Constants file for the queue service, please consider carefully where you add the constants in this file.
# Consider where to add by differentiating between constants that are not relying on other constants.
import os
from pathlib import Path


STATUS_PENDING = "PENDING"
STATUS_INITIALIZING = "INITIALIZING"
STATUS_ABORTED = "ABORTED"
STATUS_FAILED = "FAILED"
STATUS_FINISHED = "FINISHED"


# Unreferenced constants:
QUEUE_SVC_PATH = Path(__file__).resolve().parent

# Referenced constants:
HEALTH_DIR_PATH = os.path.join(QUEUE_SVC_PATH, 'health')
STATUS_LOGS_FILE = os.path.join(HEALTH_DIR_PATH, 'status.log')
