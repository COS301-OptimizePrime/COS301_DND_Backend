///
//  Generated code. Do not modify.
///
// ignore_for_file: non_constant_identifier_names,library_prefixes
library server_server_pbgrpc;

import 'dart:async';

import 'package:grpc/grpc.dart';

import 'server.pb.dart';
export 'server.pb.dart';

class SessionManagerClient extends Client {
  static final _$create = new ClientMethod<newSession, Session>(
      '/server.SessionManager/create',
      (newSession value) => value.writeToBuffer(),
      (List<int> value) => new Session.fromBuffer(value));
  static final _$join = new ClientMethod<JoinRequest, Session>(
      '/server.SessionManager/join',
      (JoinRequest value) => value.writeToBuffer(),
      (List<int> value) => new Session.fromBuffer(value));
  static final _$leave = new ClientMethod<LeaveRequest, LeaveReply>(
      '/server.SessionManager/leave',
      (LeaveRequest value) => value.writeToBuffer(),
      (List<int> value) => new LeaveReply.fromBuffer(value));
  static final _$setMax = new ClientMethod<SetMaxPlayers, Session>(
      '/server.SessionManager/setMax',
      (SetMaxPlayers value) => value.writeToBuffer(),
      (List<int> value) => new Session.fromBuffer(value));
  static final _$list = new ClientMethod<ListRequest, ListReply>(
      '/server.SessionManager/list',
      (ListRequest value) => value.writeToBuffer(),
      (List<int> value) => new ListReply.fromBuffer(value));

  SessionManagerClient(ClientChannel channel, {CallOptions options})
      : super(channel, options: options);

  ResponseFuture<Session> create(newSession request, {CallOptions options}) {
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

  ResponseFuture<Session> setMax(SetMaxPlayers request, {CallOptions options}) {
    final call = $createCall(_$setMax, new Stream.fromIterable([request]),
        options: options);
    return new ResponseFuture(call);
  }

  ResponseFuture<ListReply> list(ListRequest request, {CallOptions options}) {
    final call = $createCall(_$list, new Stream.fromIterable([request]),
        options: options);
    return new ResponseFuture(call);
  }
}

abstract class SessionManagerServiceBase extends Service {
  String get $name => 'server.SessionManager';

  SessionManagerServiceBase() {
    $addMethod(new ServiceMethod<newSession, Session>(
        'create',
        create_Pre,
        false,
        false,
        (List<int> value) => new newSession.fromBuffer(value),
        (Session value) => value.writeToBuffer()));
    $addMethod(new ServiceMethod<JoinRequest, Session>(
        'join',
        join_Pre,
        false,
        false,
        (List<int> value) => new JoinRequest.fromBuffer(value),
        (Session value) => value.writeToBuffer()));
    $addMethod(new ServiceMethod<LeaveRequest, LeaveReply>(
        'leave',
        leave_Pre,
        false,
        false,
        (List<int> value) => new LeaveRequest.fromBuffer(value),
        (LeaveReply value) => value.writeToBuffer()));
    $addMethod(new ServiceMethod<SetMaxPlayers, Session>(
        'setMax',
        setMax_Pre,
        false,
        false,
        (List<int> value) => new SetMaxPlayers.fromBuffer(value),
        (Session value) => value.writeToBuffer()));
    $addMethod(new ServiceMethod<ListRequest, ListReply>(
        'list',
        list_Pre,
        false,
        false,
        (List<int> value) => new ListRequest.fromBuffer(value),
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

  Future<ListReply> list_Pre(ServiceCall call, Future request) async {
    return list(call, await request);
  }

  Future<Session> create(ServiceCall call, newSession request);
  Future<Session> join(ServiceCall call, JoinRequest request);
  Future<LeaveReply> leave(ServiceCall call, LeaveRequest request);
  Future<Session> setMax(ServiceCall call, SetMaxPlayers request);
  Future<ListReply> list(ServiceCall call, ListRequest request);
}
