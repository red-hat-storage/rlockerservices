from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument("-sk", "--svc-kind", help="The kind of svc that is being executed")

args = parser.parse_args()


if args.svc_kind == "queue_service":
    from queue_service.queue_service import QueueService

    while True:
        with QueueService() as svc:
            svc.run()
