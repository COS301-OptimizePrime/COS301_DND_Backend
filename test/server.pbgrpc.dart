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
  static final _$list = new ClientMethod<ListRequest, ListReply>(
      '/session.SessionsManager/List',
      (ListRequest value) => value.writeToBuffer(),
      (List<int> value) => new ListReply.fromBuffer(value));
  static final _$getSessionById = new ClientMethod<GetSessionRequest, Session>(
      '/session.SessionsManager/GetSessionById',
      (GetSessionRequest value) => value.writeToBuffer(),
      (List<int> value) => new Session.fromBuffer(value));
  static final _$update = new ClientMethod<Session, Session>(
      '/session.SessionsManager/Update',
      (Session value) => value.writeToBuffer(),
      (List<int> value) => new Session.fromBuffer(value));
  static final _$kick = new ClientMethod<User, Session>(
      '/session.SessionsManager/Kick',
      (User value) => value.writeToBuffer(),
      (List<int> value) => new Session.fromBuffer(value));

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

  ResponseFuture<Session> update(Session request, {CallOptions options}) {
    final call = $createCall(_$update, new Stream.fromIterable([request]),
        options: options);
    return new ResponseFuture(call);
  }

  ResponseFuture<Session> kick(User request, {CallOptions options}) {
    final call = $createCall(_$kick, new Stream.fromIterable([request]),
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
    $addMethod(new ServiceMethod<Session, Session>(
        'Update',
        update_Pre,
        false,
        false,
        (List<int> value) => new Session.fromBuffer(value),
        (Session value) => value.writeToBuffer()));
    $addMethod(new ServiceMethod<User, Session>(
        'Kick',
        kick_Pre,
        false,
        false,
        (List<int> value) => new User.fromBuffer(value),
        (Session value) => value.writeToBuffer()));
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

  Future<ListReply> list_Pre(ServiceCall call, Future request) async {
    return list(call, await request);
  }

  Future<Session> getSessionById_Pre(ServiceCall call, Future request) async {
    return getSessionById(call, await request);
  }

  Future<Session> update_Pre(ServiceCall call, Future request) async {
    return update(call, await request);
  }

  Future<Session> kick_Pre(ServiceCall call, Future request) async {
    return kick(call, await request);
  }

  Future<Session> create(ServiceCall call, NewSessionRequest request);
  Future<Session> join(ServiceCall call, JoinRequest request);
  Future<LeaveReply> leave(ServiceCall call, LeaveRequest request);
  Future<Session> setMax(ServiceCall call, SetMaxPlayersRequest request);
  Future<ListReply> list(ServiceCall call, ListRequest request);
  Future<Session> getSessionById(ServiceCall call, GetSessionRequest request);
  Future<Session> update(ServiceCall call, Session request);
  Future<Session> kick(ServiceCall call, User request);
}