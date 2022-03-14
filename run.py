from argparse import ArgumentParser


def actions_queue_service():
    from queue_service.queue_service import QueueService

    while True:
        with QueueService() as svc:
            svc.run()


def actions_resource_sync_service():
    from resource_sync_service.resource_sync_service import ResourceSyncService

    ResourceSyncService.run_prerequisites()

    while True:
        with ResourceSyncService() as svc:
            svc.run()


action_locators = {
    "queue_service": actions_queue_service,
    "resource_sync_service": actions_resource_sync_service,
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
