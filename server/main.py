from concurrent import futures
import time

import grpc

import server_pb2
import server_pb2_grpc

from session import Session

import log
import os

#import database.db as db

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

def serve():
    logger = log.setup_custom_logger('cos301-DND')

    logger.info('Starting...')

    #logger.info("Connecting to sqlite databse...")
    #db.connect()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_pb2_grpc.add_SessionsManagerServicer_to_server(Session(), server)
    server.add_insecure_port('[::]:50051')
    server.start()

    logger.info('Started!')

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':      
    serve()
