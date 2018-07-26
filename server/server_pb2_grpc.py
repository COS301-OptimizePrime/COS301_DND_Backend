# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from . import server_pb2 as server__pb2


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
    self.Kick = channel.unary_unary(
        '/session.SessionsManager/Kick',
        request_serializer=server__pb2.KickPlayerRequest.SerializeToString,
        response_deserializer=server__pb2.Session.FromString,
        )
    self.SetName = channel.unary_unary(
        '/session.SessionsManager/SetName',
        request_serializer=server__pb2.SetNameRequest.SerializeToString,
        response_deserializer=server__pb2.Session.FromString,
        )
    self.SetPrivate = channel.unary_unary(
        '/session.SessionsManager/SetPrivate',
        request_serializer=server__pb2.SetPrivateRequest.SerializeToString,
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
    self.GetSessionsOfUser = channel.unary_unary(
        '/session.SessionsManager/GetSessionsOfUser',
        request_serializer=server__pb2.GetSessionsOfUserRequest.SerializeToString,
        response_deserializer=server__pb2.ListReply.FromString,
        )
    self.Ready = channel.unary_unary(
        '/session.SessionsManager/Ready',
        request_serializer=server__pb2.ReadyUpRequest.SerializeToString,
        response_deserializer=server__pb2.ReadyUpReply.FromString,
        )
    self.ChangeState = channel.unary_unary(
        '/session.SessionsManager/ChangeState',
        request_serializer=server__pb2.ChangeStateRequest.SerializeToString,
        response_deserializer=server__pb2.Session.FromString,
        )
    self.ChangeReadyUpExpiryTime = channel.unary_unary(
        '/session.SessionsManager/ChangeReadyUpExpiryTime',
        request_serializer=server__pb2.ChangeReadyUpExpiryTimeRequest.SerializeToString,
        response_deserializer=server__pb2.ChangeReadyUpExpiryTimeResponse.FromString,
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

  def Kick(self, request, context):
    """Kick player.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SetName(self, request, context):
    """Set the name of the session.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SetPrivate(self, request, context):
    """Set the privacy status of the session.
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

  def GetSessionsOfUser(self, request, context):
    """Get all sessions of user
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Ready(self, request, context):
    """Ready up a user in the requested session
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ChangeState(self, request, context):
    """Change session state (DM only)
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ChangeReadyUpExpiryTime(self, request, context):
    """Change the expiry time of ready up. (DM only)
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
      'Kick': grpc.unary_unary_rpc_method_handler(
          servicer.Kick,
          request_deserializer=server__pb2.KickPlayerRequest.FromString,
          response_serializer=server__pb2.Session.SerializeToString,
      ),
      'SetName': grpc.unary_unary_rpc_method_handler(
          servicer.SetName,
          request_deserializer=server__pb2.SetNameRequest.FromString,
          response_serializer=server__pb2.Session.SerializeToString,
      ),
      'SetPrivate': grpc.unary_unary_rpc_method_handler(
          servicer.SetPrivate,
          request_deserializer=server__pb2.SetPrivateRequest.FromString,
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
      'GetSessionsOfUser': grpc.unary_unary_rpc_method_handler(
          servicer.GetSessionsOfUser,
          request_deserializer=server__pb2.GetSessionsOfUserRequest.FromString,
          response_serializer=server__pb2.ListReply.SerializeToString,
      ),
      'Ready': grpc.unary_unary_rpc_method_handler(
          servicer.Ready,
          request_deserializer=server__pb2.ReadyUpRequest.FromString,
          response_serializer=server__pb2.ReadyUpReply.SerializeToString,
      ),
      'ChangeState': grpc.unary_unary_rpc_method_handler(
          servicer.ChangeState,
          request_deserializer=server__pb2.ChangeStateRequest.FromString,
          response_serializer=server__pb2.Session.SerializeToString,
      ),
      'ChangeReadyUpExpiryTime': grpc.unary_unary_rpc_method_handler(
          servicer.ChangeReadyUpExpiryTime,
          request_deserializer=server__pb2.ChangeReadyUpExpiryTimeRequest.FromString,
          response_serializer=server__pb2.ChangeReadyUpExpiryTimeResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'session.SessionsManager', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class CharactersManagerStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.CreateCharacter = channel.unary_unary(
        '/session.CharactersManager/CreateCharacter',
        request_serializer=server__pb2.NewCharacterRequest.SerializeToString,
        response_deserializer=server__pb2.Character.FromString,
        )
    self.DeleteCharacter = channel.unary_unary(
        '/session.CharactersManager/DeleteCharacter',
        request_serializer=server__pb2.DeleteCharacterRequest.SerializeToString,
        response_deserializer=server__pb2.DeleteCharacterReply.FromString,
        )
    self.GetCharacters = channel.unary_unary(
        '/session.CharactersManager/GetCharacters',
        request_serializer=server__pb2.GetCharactersRequest.SerializeToString,
        response_deserializer=server__pb2.GetCharactersReply.FromString,
        )
    self.UpdateCharacter = channel.unary_unary(
        '/session.CharactersManager/UpdateCharacter',
        request_serializer=server__pb2.UpdateCharacterRequest.SerializeToString,
        response_deserializer=server__pb2.Character.FromString,
        )
    self.GetCharacterById = channel.unary_unary(
        '/session.CharactersManager/GetCharacterById',
        request_serializer=server__pb2.GetCharacterByIdRequest.SerializeToString,
        response_deserializer=server__pb2.Character.FromString,
        )


class CharactersManagerServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def CreateCharacter(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DeleteCharacter(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetCharacters(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def UpdateCharacter(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetCharacterById(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_CharactersManagerServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'CreateCharacter': grpc.unary_unary_rpc_method_handler(
          servicer.CreateCharacter,
          request_deserializer=server__pb2.NewCharacterRequest.FromString,
          response_serializer=server__pb2.Character.SerializeToString,
      ),
      'DeleteCharacter': grpc.unary_unary_rpc_method_handler(
          servicer.DeleteCharacter,
          request_deserializer=server__pb2.DeleteCharacterRequest.FromString,
          response_serializer=server__pb2.DeleteCharacterReply.SerializeToString,
      ),
      'GetCharacters': grpc.unary_unary_rpc_method_handler(
          servicer.GetCharacters,
          request_deserializer=server__pb2.GetCharactersRequest.FromString,
          response_serializer=server__pb2.GetCharactersReply.SerializeToString,
      ),
      'UpdateCharacter': grpc.unary_unary_rpc_method_handler(
          servicer.UpdateCharacter,
          request_deserializer=server__pb2.UpdateCharacterRequest.FromString,
          response_serializer=server__pb2.Character.SerializeToString,
      ),
      'GetCharacterById': grpc.unary_unary_rpc_method_handler(
          servicer.GetCharacterById,
          request_deserializer=server__pb2.GetCharacterByIdRequest.FromString,
          response_serializer=server__pb2.Character.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'session.CharactersManager', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
