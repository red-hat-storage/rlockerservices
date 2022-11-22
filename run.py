from argparse import ArgumentParser

# Run file for the different services in this repository
# If new service is created, Create a function including the code with desired actions
# Create also a key value pair inside the action_locators dictionary


def actions_queue_service():
    from queue_service.queue_service import QueueService

    while True:
        with QueueService() as svc:
            svc.run()


action_locators = {
    "queue_service": actions_queue_service,
}

parser = ArgumentParser()
parser.add_argument(
    "-sk",
    "--svc-kind",
    choices=list(action_locators.keys()),
    help="The kind of svc that is being executed",
)

args = parser.parse_args()

# Get the desired action:
# Use [] intentionally, so it will throw Key Error exception which is good to fail a pod
func = action_locators[args.svc_kind]
func()
