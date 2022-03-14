# This file will read the status file
# This Python file will probably run as an external
# script from an orchestration platform to check liveness
# Script might needed to be executed as a module, before it uses non-relative imports
# Check out this SO poll: https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
# python -m queue_service.health.check_health
import queue_service.constants as const
import sys
from queue_service import get_time, conf


class CheckHealth:
    def __init__(self, file=const.STATUS_LOGS_FILE):
        self.file = file
        # This is the maximum amount of time that there is a possibility to not write to the log file,
        # So before quitting with code -1.
        # It's worth to wait this amount of time if something in log file has been changed
        self.max_timestamp_diff_allowed = float(
            conf["svc"].get("QUEUE_BEAT_TIMEOUT") + conf["svc"].get("INTERVAL")
        )

    def get_recent_log(self):
        """
        Get the most recent log line,
            return it as a workable python dict
        :return dict: Latest line of the log file
            with all the key value pairs
        """
        logs_as_dict = {}
        with open(self.file, "r") as f:
            log_pairs = filter(None, f.readlines()[-1].split(","))
            for pair in list(log_pairs):
                # Unpack:
                key, value = pair.split(":")
                logs_as_dict[key] = value

        return logs_as_dict

    def get_latest_healthy_timestamp(self):
        return float(self.get_recent_log().get("TIMESTAMP"))

    def get_current_timestamp(self):
        return get_time().timestamp()

    def svc_healthy(self, not_healthy_action="EXIT"):
        """
        Check if the svc is healthy by calculating the timestamps
        Take some action given the action that you want to do
            is not healthy
        :param not_healthy_action: What to do if svc unhealthy
        :return None:
        """
        timestamp_diff = (
            self.get_current_timestamp() - self.get_latest_healthy_timestamp()
        )
        if self.max_timestamp_diff_allowed > timestamp_diff:
            print("QUEUE_SVC IS HEALTHY")
        else:
            # Decide what to do depending on the not_healthy_action
            if not_healthy_action == "EXIT":
                print("QUEUE_SVC IS NOT HEALTHY")
                sys.exit(-1)


if __name__ == "__main__":
    try:
        chk = CheckHealth()
        chk.svc_healthy()
    except SystemExit:
        raise

    except Exception as e:
        # Ignore all exceptions on this external script.
        # We do not want to failure with exit code non-zero because
        # of the bugs in our code!
        # In this case, please debug locally and not on an orchestration platform!
        print("Script did not run successfully!\n" "Error is:", e)
