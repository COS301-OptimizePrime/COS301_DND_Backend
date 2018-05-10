from concurrent import futures
import time

import grpc

import server_pb2
import server_pb2_grpc

from session import Session

import signal
import log
import os

#import database.db as db

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self,signum, frame):
    self.kill_now = True

def serve():
    killer = GracefulKiller()

    logger = log.setup_custom_logger('cos301-DND')

    logger.info('Starting...')

    if os.environ['ENV'] == 'prod':
        logger.info('In production enviroment!')
    else:
        logger.info('In development enviroment!')

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_pb2_grpc.add_SessionsManagerServicer_to_server(Session(), server)
    server.add_insecure_port('[::]:50051')
    server.start()

    logger.info('Started!')

    try:
        while True:
            if killer.kill_now:
                logger.info('Received kill, stopping...')
                break
            time.sleep(1)

    except KeyboardInterrupt:
        server.stop(0)
        logger.info('Stopped!')
    finally:
        server.stop(0)
        logger.info('Stopped!')

if __name__ == '__main__':      
    serve()
