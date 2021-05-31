from rlockertools.resourcelocker import ResourceLocker
from pathlib import Path
import yaml
import os


package_dir = Path(__file__).resolve().parent
conf_location = os.path.join(package_dir, "conf.yaml")

with open(conf_location) as f:
    conf = yaml.safe_load(f)

# Resource Locker library will be instantiated against the provided environment variable
# that will be injected once the container starts.
# If it is None, it will try to use the one that is provided from the conf.yaml file
rlocker = ResourceLocker(
    instance_url=os.environ.get("RESOURCE_LOCKER_URL")
    or conf["svc"].get("RESOURCE_LOCKER_URL"),
    token=os.environ.get("RESOURCE_LOCKER_TOKEN")
    or conf["svc"].get("RESOURCE_LOCKER_TOKEN"),
)
