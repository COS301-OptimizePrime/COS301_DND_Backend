# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import server_pb2 as server__pb2


class SessionsManagerStub(object):
  """The sessions manager service definition.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Create = channel.unary_unary(
        '/session.SessionsManager/Create',
        request_serializer=server__pb2.NewSessionRequest.SerializeToString,
        response_deserializer=server__pb2.Session.FromString,
        )
    self.Join = channel.unary_unary(
        '/session.SessionsManager/Join',
        request_serializer=server__pb2.JoinRequest.SerializeToString,
        response_deserializer=server__pb2.Session.FromString,
        )
    self.Leave = channel.unary_unary(
        '/session.SessionsManager/Leave',
        request_serializer=server__pb2.LeaveRequest.SerializeToString,
        response_deserializer=server__pb2.LeaveReply.FromString,
        )
    self.SetMax = channel.unary_unary(
        '/session.SessionsManager/SetMax',
        request_serializer=server__pb2.SetMaxPlayersRequest.SerializeToString,
        response_deserializer=server__pb2.Session.FromString,
        )
    self.List = channel.unary_unary(
        '/session.SessionsManager/List',
        request_serializer=server__pb2.ListRequest.SerializeToString,
        response_deserializer=server__pb2.ListReply.FromString,
        )
    self.GetSessionById = channel.unary_unary(
        '/session.SessionsManager/GetSessionById',
        request_serializer=server__pb2.GetSessionRequest.SerializeToString,
        response_deserializer=server__pb2.Session.FromString,
        )
    self.Kick = channel.unary_unary(
        '/session.SessionsManager/Kick',
        request_serializer=server__pb2.User.SerializeToString,
        response_deserializer=server__pb2.Session.FromString,
        )


class SessionsManagerServicer(object):
  """The sessions manager service definition.
  """

  def Create(self, request, context):
    """Creates a new session.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Join(self, request, context):
    """Join a session.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Leave(self, request, context):
    """Leave a session.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SetMax(self, request, context):
    """Set the max amount of players that can be in the session.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def List(self, request, context):
    """List available sessions.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetSessionById(self, request, context):
    """Get session by ID
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Kick(self, request, context):
    """Kick player
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_SessionsManagerServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Create': grpc.unary_unary_rpc_method_handler(
          servicer.Create,
          request_deserializer=server__pb2.NewSessionRequest.FromString,
          response_serializer=server__pb2.Session.SerializeToString,
      ),
      'Join': grpc.unary_unary_rpc_method_handler(
          servicer.Join,
          request_deserializer=server__pb2.JoinRequest.FromString,
          response_serializer=server__pb2.Session.SerializeToString,
      ),
      'Leave': grpc.unary_unary_rpc_method_handler(
          servicer.Leave,
          request_deserializer=server__pb2.LeaveRequest.FromString,
          response_serializer=server__pb2.LeaveReply.SerializeToString,
      ),
      'SetMax': grpc.unary_unary_rpc_method_handler(
          servicer.SetMax,
          request_deserializer=server__pb2.SetMaxPlayersRequest.FromString,
          response_serializer=server__pb2.Session.SerializeToString,
      ),
      'List': grpc.unary_unary_rpc_method_handler(
          servicer.List,
          request_deserializer=server__pb2.ListRequest.FromString,
          response_serializer=server__pb2.ListReply.SerializeToString,
      ),
      'GetSessionById': grpc.unary_unary_rpc_method_handler(
          servicer.GetSessionById,
          request_deserializer=server__pb2.GetSessionRequest.FromString,
          response_serializer=server__pb2.Session.SerializeToString,
      ),
      'Kick': grpc.unary_unary_rpc_method_handler(
          servicer.Kick,
          request_deserializer=server__pb2.User.FromString,
          response_serializer=server__pb2.Session.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'session.SessionsManager', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
