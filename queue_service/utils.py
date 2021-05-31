import json
import sys


by_data_label = lambda q: q.data.get("label")
by_data_name = lambda q: q.data.get("name")

by_data_label_and_priority = lambda q: (q.data.get("label"), q.priority, q.id)
by_data_name_and_priority = lambda q: (q.data.get("name"), q.priority, q.id)


def json_continuously_loader(json_string, attempts=10):
    """
    WORKAROUND:
        Currently we don't know how to handle json.loads()
            Because in PostgresDB the json.loads() still might remain as string although we try to use it as dictionary
            So Sometimes the json.loads should be tried more than once.
    :param json_string:
    :return:
    """
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
