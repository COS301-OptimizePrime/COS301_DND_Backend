from concurrent import futures
import time

import grpc

import server_pb2
import server_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Session(server_pb2_grpc.SessionManagerServicer):

    def create(self, request, context):
        return server_pb2.Session(sessionId='idS!', name=request.name)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_pb2_grpc.add_SessionManagerServicer_to_server(Session(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
