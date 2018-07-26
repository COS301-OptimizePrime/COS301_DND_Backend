import os
import signal
import sys
import time
from concurrent import futures

import grpc

from server import db
from server import log
from server import server_pb2_grpc
from server.character import CharacterManager
from server.session import Session


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


def serve():
    killer = GracefulKiller()
    logger = log.setup_custom_logger("cos301-DND")

    if os.getuid() == 0:
        sys.exit("Should not be run as root!")

    logger.info("Starting...")

    if os.environ["ENV"] == "prod":
        logger.info("In production environment!")
    else:
        logger.info("In development environment!")

    logger.info("Connecting to database!")
    db.databaseConnection.getDBInstance()

    # Change between development environment and production.
    # In production
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
    server_pb2_grpc.add_SessionsManagerServicer_to_server(Session(), server)
    server_pb2_grpc.add_CharactersManagerServicer_to_server(CharacterManager(), server)
    server.add_insecure_port("[::]:50051")
    server.start()

    logger.info("Started!")

    try:
        while True:
            if killer.kill_now:
                logger.info("Received kill, stopping...")
                db.databaseConnection.close()
                break
            time.sleep(1)

    except KeyboardInterrupt:
        server.stop(0)
        logger.info("Stopped!")
    finally:
        server.stop(0)
        logger.info("Stopped!")


if __name__ == "__main__":
    serve()
