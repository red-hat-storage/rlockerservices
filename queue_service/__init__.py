from rlockertools.resourcelocker import ResourceLocker
from pathlib import Path
import yaml
import os


package_dir = Path(__file__).resolve().parent
conf_location = os.path.join(package_dir, "conf.yaml")
rlocker = ResourceLocker(
    instance_url="http://127.0.0.1:8000",
    token="8148bb8ffd6ffbc335947885eb2f3dff8c181e8f",
)
with open(conf_location) as f:
    conf = yaml.safe_load(f)
