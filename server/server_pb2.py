# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: server.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='server.proto',
  package='session',
  syntax='proto3',
  serialized_pb=_b('\n\x0cserver.proto\x12\x07session\"@\n\x18GetSessionsOfUserRequest\x12\x15\n\rauth_id_token\x18\x01 \x01(\t\x12\r\n\x05limit\x18\x02 \x01(\r\">\n\x11GetSessionRequest\x12\x15\n\rauth_id_token\x18\x01 \x01(\t\x12\x12\n\nsession_id\x18\x02 \x01(\t\"^\n\x11NewSessionRequest\x12\x15\n\rauth_id_token\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0bmax_players\x18\x03 \x01(\r\x12\x0f\n\x07private\x18\x04 \x01(\x08\"A\n\x0bListRequest\x12\x15\n\rauth_id_token\x18\x01 \x01(\t\x12\r\n\x05limit\x18\x02 \x01(\r\x12\x0c\n\x04\x66ull\x18\x03 \x01(\x08\"9\n\x0cLeaveRequest\x12\x15\n\rauth_id_token\x18\x01 \x01(\t\x12\x12\n\nsession_id\x18\x02 \x01(\t\"8\n\x0bJoinRequest\x12\x15\n\rauth_id_token\x18\x01 \x01(\t\x12\x12\n\nsession_id\x18\x02 \x01(\t\"[\n\x11KickPlayerRequest\x12\x15\n\rauth_id_token\x18\x01 \x01(\t\x12\x12\n\nsession_id\x18\x02 \x01(\t\x12\x1b\n\x04user\x18\x03 \x01(\x0b\x32\r.session.User\"O\n\x11SetPrivateRequest\x12\x15\n\rauth_id_token\x18\x01 \x01(\t\x12\x12\n\nsession_id\x18\x02 \x01(\t\x12\x0f\n\x07private\x18\x03 \x01(\x08\"Q\n\x14SetMaxPlayersRequest\x12\x15\n\rauth_id_token\x18\x01 \x01(\t\x12\x0e\n\x06number\x18\x02 \x01(\r\x12\x12\n\nsession_id\x18\x03 \x01(\t\"I\n\x0eSetNameRequest\x12\x15\n\rauth_id_token\x18\x01 \x01(\t\x12\x12\n\nsession_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\"?\n\tListReply\x12\"\n\x08sessions\x18\x01 \x03(\x0b\x32\x10.session.Session\x12\x0e\n\x06status\x18\x02 \x01(\t\"4\n\nLeaveReply\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x16\n\x0estatus_message\x18\x02 \x01(\t\"\xe2\x01\n\x07Session\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x16\n\x0estatus_message\x18\x02 \x01(\t\x12\x12\n\nsession_id\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\x12%\n\x0e\x64ungeon_master\x18\x05 \x01(\x0b\x32\r.session.User\x12\x14\n\x0c\x64\x61te_created\x18\x06 \x01(\t\x12\x13\n\x0bmax_players\x18\x07 \x01(\r\x12\x1c\n\x05users\x18\x08 \x03(\x0b\x32\r.session.User\x12\x0f\n\x07private\x18\t \x01(\x08\x12\x0c\n\x04\x66ull\x18\n \x01(\x08\"!\n\x04User\x12\x0b\n\x03uid\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t2\xe3\x04\n\x0fSessionsManager\x12\x38\n\x06\x43reate\x12\x1a.session.NewSessionRequest\x1a\x10.session.Session\"\x00\x12\x30\n\x04Join\x12\x14.session.JoinRequest\x1a\x10.session.Session\"\x00\x12\x35\n\x05Leave\x12\x15.session.LeaveRequest\x1a\x13.session.LeaveReply\"\x00\x12;\n\x06SetMax\x12\x1d.session.SetMaxPlayersRequest\x1a\x10.session.Session\"\x00\x12\x36\n\x04Kick\x12\x1a.session.KickPlayerRequest\x1a\x10.session.Session\"\x00\x12\x36\n\x07SetName\x12\x17.session.SetNameRequest\x1a\x10.session.Session\"\x00\x12<\n\nSetPrivate\x12\x1a.session.SetPrivateRequest\x1a\x10.session.Session\"\x00\x12\x32\n\x04List\x12\x14.session.ListRequest\x1a\x12.session.ListReply\"\x00\x12@\n\x0eGetSessionById\x12\x1a.session.GetSessionRequest\x1a\x10.session.Session\"\x00\x12L\n\x11GetSessionsOfUser\x12!.session.GetSessionsOfUserRequest\x1a\x12.session.ListReply\"\x00\x62\x06proto3')
)




_GETSESSIONSOFUSERREQUEST = _descriptor.Descriptor(
  name='GetSessionsOfUserRequest',
  full_name='session.GetSessionsOfUserRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='auth_id_token', full_name='session.GetSessionsOfUserRequest.auth_id_token', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='limit', full_name='session.GetSessionsOfUserRequest.limit', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=25,
  serialized_end=89,
)


_GETSESSIONREQUEST = _descriptor.Descriptor(
  name='GetSessionRequest',
  full_name='session.GetSessionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='auth_id_token', full_name='session.GetSessionRequest.auth_id_token', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='session_id', full_name='session.GetSessionRequest.session_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=91,
  serialized_end=153,
)


_NEWSESSIONREQUEST = _descriptor.Descriptor(
  name='NewSessionRequest',
  full_name='session.NewSessionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='auth_id_token', full_name='session.NewSessionRequest.auth_id_token', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='session.NewSessionRequest.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='max_players', full_name='session.NewSessionRequest.max_players', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='private', full_name='session.NewSessionRequest.private', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=155,
  serialized_end=249,
)


_LISTREQUEST = _descriptor.Descriptor(
  name='ListRequest',
  full_name='session.ListRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='auth_id_token', full_name='session.ListRequest.auth_id_token', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='limit', full_name='session.ListRequest.limit', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='full', full_name='session.ListRequest.full', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=251,
  serialized_end=316,
)


_LEAVEREQUEST = _descriptor.Descriptor(
  name='LeaveRequest',
  full_name='session.LeaveRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='auth_id_token', full_name='session.LeaveRequest.auth_id_token', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='session_id', full_name='session.LeaveRequest.session_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=318,
  serialized_end=375,
)


_JOINREQUEST = _descriptor.Descriptor(
  name='JoinRequest',
  full_name='session.JoinRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='auth_id_token', full_name='session.JoinRequest.auth_id_token', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='session_id', full_name='session.JoinRequest.session_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=377,
  serialized_end=433,
)


_KICKPLAYERREQUEST = _descriptor.Descriptor(
  name='KickPlayerRequest',
  full_name='session.KickPlayerRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='auth_id_token', full_name='session.KickPlayerRequest.auth_id_token', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='session_id', full_name='session.KickPlayerRequest.session_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='user', full_name='session.KickPlayerRequest.user', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=435,
  serialized_end=526,
)


_SETPRIVATEREQUEST = _descriptor.Descriptor(
  name='SetPrivateRequest',
  full_name='session.SetPrivateRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='auth_id_token', full_name='session.SetPrivateRequest.auth_id_token', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='session_id', full_name='session.SetPrivateRequest.session_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='private', full_name='session.SetPrivateRequest.private', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=528,
  serialized_end=607,
)


_SETMAXPLAYERSREQUEST = _descriptor.Descriptor(
  name='SetMaxPlayersRequest',
  full_name='session.SetMaxPlayersRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='auth_id_token', full_name='session.SetMaxPlayersRequest.auth_id_token', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='number', full_name='session.SetMaxPlayersRequest.number', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='session_id', full_name='session.SetMaxPlayersRequest.session_id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=609,
  serialized_end=690,
)


_SETNAMEREQUEST = _descriptor.Descriptor(
  name='SetNameRequest',
  full_name='session.SetNameRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='auth_id_token', full_name='session.SetNameRequest.auth_id_token', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='session_id', full_name='session.SetNameRequest.session_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='session.SetNameRequest.name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=692,
  serialized_end=765,
)


_LISTREPLY = _descriptor.Descriptor(
  name='ListReply',
  full_name='session.ListReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sessions', full_name='session.ListReply.sessions', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='session.ListReply.status', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=767,
  serialized_end=830,
)


_LEAVEREPLY = _descriptor.Descriptor(
  name='LeaveReply',
  full_name='session.LeaveReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='session.LeaveReply.status', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status_message', full_name='session.LeaveReply.status_message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=832,
  serialized_end=884,
)


_SESSION = _descriptor.Descriptor(
  name='Session',
  full_name='session.Session',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='session.Session.status', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status_message', full_name='session.Session.status_message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='session_id', full_name='session.Session.session_id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='session.Session.name', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='dungeon_master', full_name='session.Session.dungeon_master', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='date_created', full_name='session.Session.date_created', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='max_players', full_name='session.Session.max_players', index=6,
      number=7, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='users', full_name='session.Session.users', index=7,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='private', full_name='session.Session.private', index=8,
      number=9, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='full', full_name='session.Session.full', index=9,
      number=10, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=887,
  serialized_end=1113,
)


_USER = _descriptor.Descriptor(
  name='User',
  full_name='session.User',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uid', full_name='session.User.uid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='session.User.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1115,
  serialized_end=1148,
)

_KICKPLAYERREQUEST.fields_by_name['user'].message_type = _USER
_LISTREPLY.fields_by_name['sessions'].message_type = _SESSION
_SESSION.fields_by_name['dungeon_master'].message_type = _USER
_SESSION.fields_by_name['users'].message_type = _USER
DESCRIPTOR.message_types_by_name['GetSessionsOfUserRequest'] = _GETSESSIONSOFUSERREQUEST
DESCRIPTOR.message_types_by_name['GetSessionRequest'] = _GETSESSIONREQUEST
DESCRIPTOR.message_types_by_name['NewSessionRequest'] = _NEWSESSIONREQUEST
DESCRIPTOR.message_types_by_name['ListRequest'] = _LISTREQUEST
DESCRIPTOR.message_types_by_name['LeaveRequest'] = _LEAVEREQUEST
DESCRIPTOR.message_types_by_name['JoinRequest'] = _JOINREQUEST
DESCRIPTOR.message_types_by_name['KickPlayerRequest'] = _KICKPLAYERREQUEST
DESCRIPTOR.message_types_by_name['SetPrivateRequest'] = _SETPRIVATEREQUEST
DESCRIPTOR.message_types_by_name['SetMaxPlayersRequest'] = _SETMAXPLAYERSREQUEST
DESCRIPTOR.message_types_by_name['SetNameRequest'] = _SETNAMEREQUEST
DESCRIPTOR.message_types_by_name['ListReply'] = _LISTREPLY
DESCRIPTOR.message_types_by_name['LeaveReply'] = _LEAVEREPLY
DESCRIPTOR.message_types_by_name['Session'] = _SESSION
DESCRIPTOR.message_types_by_name['User'] = _USER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetSessionsOfUserRequest = _reflection.GeneratedProtocolMessageType('GetSessionsOfUserRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETSESSIONSOFUSERREQUEST,
  __module__ = 'server_pb2'
  # @@protoc_insertion_point(class_scope:session.GetSessionsOfUserRequest)
  ))
_sym_db.RegisterMessage(GetSessionsOfUserRequest)

GetSessionRequest = _reflection.GeneratedProtocolMessageType('GetSessionRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETSESSIONREQUEST,
  __module__ = 'server_pb2'
  # @@protoc_insertion_point(class_scope:session.GetSessionRequest)
  ))
_sym_db.RegisterMessage(GetSessionRequest)

NewSessionRequest = _reflection.GeneratedProtocolMessageType('NewSessionRequest', (_message.Message,), dict(
  DESCRIPTOR = _NEWSESSIONREQUEST,
  __module__ = 'server_pb2'
  # @@protoc_insertion_point(class_scope:session.NewSessionRequest)
  ))
_sym_db.RegisterMessage(NewSessionRequest)

ListRequest = _reflection.GeneratedProtocolMessageType('ListRequest', (_message.Message,), dict(
  DESCRIPTOR = _LISTREQUEST,
  __module__ = 'server_pb2'
  # @@protoc_insertion_point(class_scope:session.ListRequest)
  ))
_sym_db.RegisterMessage(ListRequest)

LeaveRequest = _reflection.GeneratedProtocolMessageType('LeaveRequest', (_message.Message,), dict(
  DESCRIPTOR = _LEAVEREQUEST,
  __module__ = 'server_pb2'
  # @@protoc_insertion_point(class_scope:session.LeaveRequest)
  ))
_sym_db.RegisterMessage(LeaveRequest)

JoinRequest = _reflection.GeneratedProtocolMessageType('JoinRequest', (_message.Message,), dict(
  DESCRIPTOR = _JOINREQUEST,
  __module__ = 'server_pb2'
  # @@protoc_insertion_point(class_scope:session.JoinRequest)
  ))
_sym_db.RegisterMessage(JoinRequest)

KickPlayerRequest = _reflection.GeneratedProtocolMessageType('KickPlayerRequest', (_message.Message,), dict(
  DESCRIPTOR = _KICKPLAYERREQUEST,
  __module__ = 'server_pb2'
  # @@protoc_insertion_point(class_scope:session.KickPlayerRequest)
  ))
_sym_db.RegisterMessage(KickPlayerRequest)

SetPrivateRequest = _reflection.GeneratedProtocolMessageType('SetPrivateRequest', (_message.Message,), dict(
  DESCRIPTOR = _SETPRIVATEREQUEST,
  __module__ = 'server_pb2'
  # @@protoc_insertion_point(class_scope:session.SetPrivateRequest)
  ))
_sym_db.RegisterMessage(SetPrivateRequest)

SetMaxPlayersRequest = _reflection.GeneratedProtocolMessageType('SetMaxPlayersRequest', (_message.Message,), dict(
  DESCRIPTOR = _SETMAXPLAYERSREQUEST,
  __module__ = 'server_pb2'
  # @@protoc_insertion_point(class_scope:session.SetMaxPlayersRequest)
  ))
_sym_db.RegisterMessage(SetMaxPlayersRequest)

SetNameRequest = _reflection.GeneratedProtocolMessageType('SetNameRequest', (_message.Message,), dict(
  DESCRIPTOR = _SETNAMEREQUEST,
  __module__ = 'server_pb2'
  # @@protoc_insertion_point(class_scope:session.SetNameRequest)
  ))
_sym_db.RegisterMessage(SetNameRequest)

ListReply = _reflection.GeneratedProtocolMessageType('ListReply', (_message.Message,), dict(
  DESCRIPTOR = _LISTREPLY,
  __module__ = 'server_pb2'
  # @@protoc_insertion_point(class_scope:session.ListReply)
  ))
_sym_db.RegisterMessage(ListReply)

LeaveReply = _reflection.GeneratedProtocolMessageType('LeaveReply', (_message.Message,), dict(
  DESCRIPTOR = _LEAVEREPLY,
  __module__ = 'server_pb2'
  # @@protoc_insertion_point(class_scope:session.LeaveReply)
  ))
_sym_db.RegisterMessage(LeaveReply)

Session = _reflection.GeneratedProtocolMessageType('Session', (_message.Message,), dict(
  DESCRIPTOR = _SESSION,
  __module__ = 'server_pb2'
  # @@protoc_insertion_point(class_scope:session.Session)
  ))
_sym_db.RegisterMessage(Session)

User = _reflection.GeneratedProtocolMessageType('User', (_message.Message,), dict(
  DESCRIPTOR = _USER,
  __module__ = 'server_pb2'
  # @@protoc_insertion_point(class_scope:session.User)
  ))
_sym_db.RegisterMessage(User)



_SESSIONSMANAGER = _descriptor.ServiceDescriptor(
  name='SessionsManager',
  full_name='session.SessionsManager',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=1151,
  serialized_end=1762,
  methods=[
  _descriptor.MethodDescriptor(
    name='Create',
    full_name='session.SessionsManager.Create',
    index=0,
    containing_service=None,
    input_type=_NEWSESSIONREQUEST,
    output_type=_SESSION,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Join',
    full_name='session.SessionsManager.Join',
    index=1,
    containing_service=None,
    input_type=_JOINREQUEST,
    output_type=_SESSION,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Leave',
    full_name='session.SessionsManager.Leave',
    index=2,
    containing_service=None,
    input_type=_LEAVEREQUEST,
    output_type=_LEAVEREPLY,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SetMax',
    full_name='session.SessionsManager.SetMax',
    index=3,
    containing_service=None,
    input_type=_SETMAXPLAYERSREQUEST,
    output_type=_SESSION,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Kick',
    full_name='session.SessionsManager.Kick',
    index=4,
    containing_service=None,
    input_type=_KICKPLAYERREQUEST,
    output_type=_SESSION,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SetName',
    full_name='session.SessionsManager.SetName',
    index=5,
    containing_service=None,
    input_type=_SETNAMEREQUEST,
    output_type=_SESSION,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SetPrivate',
    full_name='session.SessionsManager.SetPrivate',
    index=6,
    containing_service=None,
    input_type=_SETPRIVATEREQUEST,
    output_type=_SESSION,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='List',
    full_name='session.SessionsManager.List',
    index=7,
    containing_service=None,
    input_type=_LISTREQUEST,
    output_type=_LISTREPLY,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetSessionById',
    full_name='session.SessionsManager.GetSessionById',
    index=8,
    containing_service=None,
    input_type=_GETSESSIONREQUEST,
    output_type=_SESSION,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetSessionsOfUser',
    full_name='session.SessionsManager.GetSessionsOfUser',
    index=9,
    containing_service=None,
    input_type=_GETSESSIONSOFUSERREQUEST,
    output_type=_LISTREPLY,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_SESSIONSMANAGER)

DESCRIPTOR.services_by_name['SessionsManager'] = _SESSIONSMANAGER

# @@protoc_insertion_point(module_scope)
