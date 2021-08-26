from queue_service.connection import ResourceLockerConnection
import json
import sys
import time
import datetime


by_data_label = lambda q: q.data.get("label")
by_data_name = lambda q: q.data.get("name")

by_data_label_and_priority = lambda q: (q.data.get("label"), q.priority, q.id)
by_data_name_and_priority = lambda q: (q.data.get("name"), q.priority, q.id)


rlocker = ResourceLockerConnection()

def json_continuously_loader(json_string, attempts=10):
    """
    WORKAROUND:
        Currently we don't know how to handle json.loads()
            Because in PostgresDB the json.loads() still might remain as string although we try to use it as dictionary
            So Sometimes the json.loads should be tried more than once.
    :param json_string:
    :return:
    """
    if type(json_string) == dict:
        return json_string

    loaded_json = None
    attempts = list(range(1, attempts + 1, 1))
    for attempt in attempts:
        try:
            loaded_json = json.loads(json_string)
            dict(
                loaded_json
            )  # Should fail with value error if this is still NOT a dictionary
            return loaded_json  # If it is a python dictionary, lets return it
        except ValueError:
            if attempt != attempts[-1]:
                print(
                    "The loaded json is still not a dictionary, trying to parse again the same json ... \n"
                )
                json_string = loaded_json
                print(loaded_json)
            else:
                # If after 10 tries, we we're not able to return loaded_json, something went wrong.
                # Let's RAISE the original error
                print("Unexpected error:", sys.exc_info()[0])
                raise

def calculate_time_diff_str(fmt, s1, s2):
    '''
    Calculate the differences by SECONDS between two time ranges,
        in a given format
    :param fmt:
    :param dt1:
    :param dt2:
    :return:
    '''
    tdelta = datetime.datetime.strptime(s2, fmt) - datetime.datetime.strptime(s1, fmt)
    return tdelta.seconds

def queue_has_beat(
        queue_id,
        in_last_x_seconds=600,
        interval=1
):
    '''
    Before releasing the queue and locking the service, it is important
    to check that the queue has beat from a client.
    Because, if there is no beat by a client, a queue could be locked without having
        a client that waits for that queue
    And there is no reason to lock any resource if there is no beat by a client, it should be
        aborted if there was no beat in the last x seconds
    :param queue_id:
    :param in_last_x_seconds:
    :param interval:
    :return:
    '''
    FMT = '%Y-%m-%d %H:%M:%S'
    time_diffs = []
    for _ in range(in_last_x_seconds):
        queue_obj = rlocker.get_queue(queue_id)

        now = datetime.datetime.utcnow().strftime(FMT)

        # If the following is none, then it also means that there is no beat,
        # In order to not break the logic of parsing str to datetime, it's a great idea to pass in
        # some old date.
        # And then the seconds calculation will still work
        queue_last_beat = queue_obj.get('last_beat')
        if queue_last_beat in [None, "None"]:
            queue_last_beat = "1970-01-01T00:00:00.000000Z"

        try:
            queue_last_beat_fmt_str = datetime.datetime.strptime(
                queue_last_beat,
                "%Y-%m-%dT%H:%M:%S.%f%z" # This is the only format that supports to read the time from JSON
            ).strftime(FMT)
        except ValueError:
            queue_last_beat_fmt_str = datetime.datetime.strptime(
                queue_last_beat,
                "%Y-%m-%dT%H:%M:%S%z" # This is the only format that supports to read from JSON, once the time is edited from admin panel!
            ).strftime(FMT)

        last_beat_in_seconds = calculate_time_diff_str(
            FMT,
            s1=queue_last_beat_fmt_str,
            s2=now
        )
        if not last_beat_in_seconds <= min(time_diffs, default=1):
            time_diffs.append(last_beat_in_seconds)
            print(f"{queue_obj.get('id')} did not beat for {last_beat_in_seconds} seconds ... ")
            time.sleep(interval)
        else:
            return True

    else:
        return False

