///
//  Generated code. Do not modify.
///
// ignore_for_file: non_constant_identifier_names,library_prefixes
library session_server_pbgrpc;

import 'dart:async';

import 'package:grpc/grpc.dart';

import 'server.pb.dart';
export 'server.pb.dart';

class SessionsManagerClient extends Client {
  static final _$create = new ClientMethod<NewSessionRequest, Session>(
      '/session.SessionsManager/Create',
      (NewSessionRequest value) => value.writeToBuffer(),
      (List<int> value) => new Session.fromBuffer(value));
  static final _$join = new ClientMethod<JoinRequest, Session>(
      '/session.SessionsManager/Join',
      (JoinRequest value) => value.writeToBuffer(),
      (List<int> value) => new Session.fromBuffer(value));
  static final _$leave = new ClientMethod<LeaveRequest, LeaveReply>(
      '/session.SessionsManager/Leave',
      (LeaveRequest value) => value.writeToBuffer(),
      (List<int> value) => new LeaveReply.fromBuffer(value));
  static final _$setMax = new ClientMethod<SetMaxPlayersRequest, Session>(
      '/session.SessionsManager/SetMax',
      (SetMaxPlayersRequest value) => value.writeToBuffer(),
      (List<int> value) => new Session.fromBuffer(value));
  static final _$kick = new ClientMethod<KickPlayerRequest, Session>(
      '/session.SessionsManager/Kick',
      (KickPlayerRequest value) => value.writeToBuffer(),
      (List<int> value) => new Session.fromBuffer(value));
  static final _$setName = new ClientMethod<SetNameRequest, Session>(
      '/session.SessionsManager/SetName',
      (SetNameRequest value) => value.writeToBuffer(),
      (List<int> value) => new Session.fromBuffer(value));
  static final _$setPrivate = new ClientMethod<SetPrivateRequest, Session>(
      '/session.SessionsManager/SetPrivate',
      (SetPrivateRequest value) => value.writeToBuffer(),
      (List<int> value) => new Session.fromBuffer(value));
  static final _$list = new ClientMethod<ListRequest, ListReply>(
      '/session.SessionsManager/List',
      (ListRequest value) => value.writeToBuffer(),
      (List<int> value) => new ListReply.fromBuffer(value));
  static final _$getSessionById = new ClientMethod<GetSessionRequest, Session>(
      '/session.SessionsManager/GetSessionById',
      (GetSessionRequest value) => value.writeToBuffer(),
      (List<int> value) => new Session.fromBuffer(value));
  static final _$getSessionsOfUser =
      new ClientMethod<GetSessionsOfUserRequest, ListReply>(
          '/session.SessionsManager/GetSessionsOfUser',
          (GetSessionsOfUserRequest value) => value.writeToBuffer(),
          (List<int> value) => new ListReply.fromBuffer(value));

  SessionsManagerClient(ClientChannel channel, {CallOptions options})
      : super(channel, options: options);

  ResponseFuture<Session> create(NewSessionRequest request,
      {CallOptions options}) {
    final call = $createCall(_$create, new Stream.fromIterable([request]),
        options: options);
    return new ResponseFuture(call);
  }

  ResponseFuture<Session> join(JoinRequest request, {CallOptions options}) {
    final call = $createCall(_$join, new Stream.fromIterable([request]),
        options: options);
    return new ResponseFuture(call);
  }

  ResponseFuture<LeaveReply> leave(LeaveRequest request,
      {CallOptions options}) {
    final call = $createCall(_$leave, new Stream.fromIterable([request]),
        options: options);
    return new ResponseFuture(call);
  }

  ResponseFuture<Session> setMax(SetMaxPlayersRequest request,
      {CallOptions options}) {
    final call = $createCall(_$setMax, new Stream.fromIterable([request]),
        options: options);
    return new ResponseFuture(call);
  }

  ResponseFuture<Session> kick(KickPlayerRequest request,
      {CallOptions options}) {
    final call = $createCall(_$kick, new Stream.fromIterable([request]),
        options: options);
    return new ResponseFuture(call);
  }

  ResponseFuture<Session> setName(SetNameRequest request,
      {CallOptions options}) {
    final call = $createCall(_$setName, new Stream.fromIterable([request]),
        options: options);
    return new ResponseFuture(call);
  }

  ResponseFuture<Session> setPrivate(SetPrivateRequest request,
      {CallOptions options}) {
    final call = $createCall(_$setPrivate, new Stream.fromIterable([request]),
        options: options);
    return new ResponseFuture(call);
  }

  ResponseFuture<ListReply> list(ListRequest request, {CallOptions options}) {
    final call = $createCall(_$list, new Stream.fromIterable([request]),
        options: options);
    return new ResponseFuture(call);
  }

  ResponseFuture<Session> getSessionById(GetSessionRequest request,
      {CallOptions options}) {
    final call = $createCall(
        _$getSessionById, new Stream.fromIterable([request]),
        options: options);
    return new ResponseFuture(call);
  }

  ResponseFuture<ListReply> getSessionsOfUser(GetSessionsOfUserRequest request,
      {CallOptions options}) {
    final call = $createCall(
        _$getSessionsOfUser, new Stream.fromIterable([request]),
        options: options);
    return new ResponseFuture(call);
  }
}

abstract class SessionsManagerServiceBase extends Service {
  String get $name => 'session.SessionsManager';

  SessionsManagerServiceBase() {
    $addMethod(new ServiceMethod<NewSessionRequest, Session>(
        'Create',
        create_Pre,
        false,
        false,
        (List<int> value) => new NewSessionRequest.fromBuffer(value),
        (Session value) => value.writeToBuffer()));
    $addMethod(new ServiceMethod<JoinRequest, Session>(
        'Join',
        join_Pre,
        false,
        false,
        (List<int> value) => new JoinRequest.fromBuffer(value),
        (Session value) => value.writeToBuffer()));
    $addMethod(new ServiceMethod<LeaveRequest, LeaveReply>(
        'Leave',
        leave_Pre,
        false,
        false,
        (List<int> value) => new LeaveRequest.fromBuffer(value),
        (LeaveReply value) => value.writeToBuffer()));
    $addMethod(new ServiceMethod<SetMaxPlayersRequest, Session>(
        'SetMax',
        setMax_Pre,
        false,
        false,
        (List<int> value) => new SetMaxPlayersRequest.fromBuffer(value),
        (Session value) => value.writeToBuffer()));
    $addMethod(new ServiceMethod<KickPlayerRequest, Session>(
        'Kick',
        kick_Pre,
        false,
        false,
        (List<int> value) => new KickPlayerRequest.fromBuffer(value),
        (Session value) => value.writeToBuffer()));
    $addMethod(new ServiceMethod<SetNameRequest, Session>(
        'SetName',
        setName_Pre,
        false,
        false,
        (List<int> value) => new SetNameRequest.fromBuffer(value),
        (Session value) => value.writeToBuffer()));
    $addMethod(new ServiceMethod<SetPrivateRequest, Session>(
        'SetPrivate',
        setPrivate_Pre,
        false,
        false,
        (List<int> value) => new SetPrivateRequest.fromBuffer(value),
        (Session value) => value.writeToBuffer()));
    $addMethod(new ServiceMethod<ListRequest, ListReply>(
        'List',
        list_Pre,
        false,
        false,
        (List<int> value) => new ListRequest.fromBuffer(value),
        (ListReply value) => value.writeToBuffer()));
    $addMethod(new ServiceMethod<GetSessionRequest, Session>(
        'GetSessionById',
        getSessionById_Pre,
        false,
        false,
        (List<int> value) => new GetSessionRequest.fromBuffer(value),
        (Session value) => value.writeToBuffer()));
    $addMethod(new ServiceMethod<GetSessionsOfUserRequest, ListReply>(
        'GetSessionsOfUser',
        getSessionsOfUser_Pre,
        false,
        false,
        (List<int> value) => new GetSessionsOfUserRequest.fromBuffer(value),
        (ListReply value) => value.writeToBuffer()));
  }

  Future<Session> create_Pre(ServiceCall call, Future request) async {
    return create(call, await request);
  }

  Future<Session> join_Pre(ServiceCall call, Future request) async {
    return join(call, await request);
  }

  Future<LeaveReply> leave_Pre(ServiceCall call, Future request) async {
    return leave(call, await request);
  }

  Future<Session> setMax_Pre(ServiceCall call, Future request) async {
    return setMax(call, await request);
  }

  Future<Session> kick_Pre(ServiceCall call, Future request) async {
    return kick(call, await request);
  }

  Future<Session> setName_Pre(ServiceCall call, Future request) async {
    return setName(call, await request);
  }

  Future<Session> setPrivate_Pre(ServiceCall call, Future request) async {
    return setPrivate(call, await request);
  }

  Future<ListReply> list_Pre(ServiceCall call, Future request) async {
    return list(call, await request);
  }

  Future<Session> getSessionById_Pre(ServiceCall call, Future request) async {
    return getSessionById(call, await request);
  }

  Future<ListReply> getSessionsOfUser_Pre(
      ServiceCall call, Future request) async {
    return getSessionsOfUser(call, await request);
  }

  Future<Session> create(ServiceCall call, NewSessionRequest request);
  Future<Session> join(ServiceCall call, JoinRequest request);
  Future<LeaveReply> leave(ServiceCall call, LeaveRequest request);
  Future<Session> setMax(ServiceCall call, SetMaxPlayersRequest request);
  Future<Session> kick(ServiceCall call, KickPlayerRequest request);
  Future<Session> setName(ServiceCall call, SetNameRequest request);
  Future<Session> setPrivate(ServiceCall call, SetPrivateRequest request);
  Future<ListReply> list(ServiceCall call, ListRequest request);
  Future<Session> getSessionById(ServiceCall call, GetSessionRequest request);
  Future<ListReply> getSessionsOfUser(
      ServiceCall call, GetSessionsOfUserRequest request);
}

class CharactersManagerClient extends Client {
  static final _$createCharacter =
      new ClientMethod<NewCharacterRequest, Character>(
          '/session.CharactersManager/CreateCharacter',
          (NewCharacterRequest value) => value.writeToBuffer(),
          (List<int> value) => new Character.fromBuffer(value));
  static final _$deleteCharacter =
      new ClientMethod<Character, DeleteCharacterReply>(
          '/session.CharactersManager/DeleteCharacter',
          (Character value) => value.writeToBuffer(),
          (List<int> value) => new DeleteCharacterReply.fromBuffer(value));

  CharactersManagerClient(ClientChannel channel, {CallOptions options})
      : super(channel, options: options);

  ResponseFuture<Character> createCharacter(NewCharacterRequest request,
      {CallOptions options}) {
    final call = $createCall(
        _$createCharacter, new Stream.fromIterable([request]),
        options: options);
    return new ResponseFuture(call);
  }

  ResponseFuture<DeleteCharacterReply> deleteCharacter(Character request,
      {CallOptions options}) {
    final call = $createCall(
        _$deleteCharacter, new Stream.fromIterable([request]),
        options: options);
    return new ResponseFuture(call);
  }
}

abstract class CharactersManagerServiceBase extends Service {
  String get $name => 'session.CharactersManager';

  CharactersManagerServiceBase() {
    $addMethod(new ServiceMethod<NewCharacterRequest, Character>(
        'CreateCharacter',
        createCharacter_Pre,
        false,
        false,
        (List<int> value) => new NewCharacterRequest.fromBuffer(value),
        (Character value) => value.writeToBuffer()));
    $addMethod(new ServiceMethod<Character, DeleteCharacterReply>(
        'DeleteCharacter',
        deleteCharacter_Pre,
        false,
        false,
        (List<int> value) => new Character.fromBuffer(value),
        (DeleteCharacterReply value) => value.writeToBuffer()));
  }

  Future<Character> createCharacter_Pre(
      ServiceCall call, Future request) async {
    return createCharacter(call, await request);
  }

  Future<DeleteCharacterReply> deleteCharacter_Pre(
      ServiceCall call, Future request) async {
    return deleteCharacter(call, await request);
  }

  Future<Character> createCharacter(
      ServiceCall call, NewCharacterRequest request);
  Future<DeleteCharacterReply> deleteCharacter(
      ServiceCall call, Character request);
}
