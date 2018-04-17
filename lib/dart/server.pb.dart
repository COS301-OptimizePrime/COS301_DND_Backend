///
//  Generated code. Do not modify.
///
// ignore_for_file: non_constant_identifier_names,library_prefixes
library server_server;

// ignore: UNUSED_SHOWN_NAME
import 'dart:core' show int, bool, double, String, List, override;

import 'package:protobuf/protobuf.dart';

class newSession extends GeneratedMessage {
  static final BuilderInfo _i = new BuilderInfo('newSession')
    ..aOS(1, 'name')
    ..hasRequiredFields = false
  ;

  newSession() : super();
  newSession.fromBuffer(List<int> i, [ExtensionRegistry r = ExtensionRegistry.EMPTY]) : super.fromBuffer(i, r);
  newSession.fromJson(String i, [ExtensionRegistry r = ExtensionRegistry.EMPTY]) : super.fromJson(i, r);
  newSession clone() => new newSession()..mergeFromMessage(this);
  BuilderInfo get info_ => _i;
  static newSession create() => new newSession();
  static PbList<newSession> createRepeated() => new PbList<newSession>();
  static newSession getDefault() {
    if (_defaultInstance == null) _defaultInstance = new _ReadonlynewSession();
    return _defaultInstance;
  }
  static newSession _defaultInstance;
  static void $checkItem(newSession v) {
    if (v is! newSession) checkItemFailed(v, 'newSession');
  }

  String get name => $_getS(0, '');
  set name(String v) { $_setString(0, v); }
  bool hasName() => $_has(0);
  void clearName() => clearField(1);
}

class _ReadonlynewSession extends newSession with ReadonlyMessageMixin {}

class ListRequest extends GeneratedMessage {
  static final BuilderInfo _i = new BuilderInfo('ListRequest')
    ..a<int>(1, 'limit', PbFieldType.OU3)
    ..hasRequiredFields = false
  ;

  ListRequest() : super();
  ListRequest.fromBuffer(List<int> i, [ExtensionRegistry r = ExtensionRegistry.EMPTY]) : super.fromBuffer(i, r);
  ListRequest.fromJson(String i, [ExtensionRegistry r = ExtensionRegistry.EMPTY]) : super.fromJson(i, r);
  ListRequest clone() => new ListRequest()..mergeFromMessage(this);
  BuilderInfo get info_ => _i;
  static ListRequest create() => new ListRequest();
  static PbList<ListRequest> createRepeated() => new PbList<ListRequest>();
  static ListRequest getDefault() {
    if (_defaultInstance == null) _defaultInstance = new _ReadonlyListRequest();
    return _defaultInstance;
  }
  static ListRequest _defaultInstance;
  static void $checkItem(ListRequest v) {
    if (v is! ListRequest) checkItemFailed(v, 'ListRequest');
  }

  int get limit => $_get(0, 0);
  set limit(int v) { $_setUnsignedInt32(0, v); }
  bool hasLimit() => $_has(0);
  void clearLimit() => clearField(1);
}

class _ReadonlyListRequest extends ListRequest with ReadonlyMessageMixin {}

class ListReply extends GeneratedMessage {
  static final BuilderInfo _i = new BuilderInfo('ListReply')
    ..pp<Session>(1, 'sessions', PbFieldType.PM, Session.$checkItem, Session.create)
    ..hasRequiredFields = false
  ;

  ListReply() : super();
  ListReply.fromBuffer(List<int> i, [ExtensionRegistry r = ExtensionRegistry.EMPTY]) : super.fromBuffer(i, r);
  ListReply.fromJson(String i, [ExtensionRegistry r = ExtensionRegistry.EMPTY]) : super.fromJson(i, r);
  ListReply clone() => new ListReply()..mergeFromMessage(this);
  BuilderInfo get info_ => _i;
  static ListReply create() => new ListReply();
  static PbList<ListReply> createRepeated() => new PbList<ListReply>();
  static ListReply getDefault() {
    if (_defaultInstance == null) _defaultInstance = new _ReadonlyListReply();
    return _defaultInstance;
  }
  static ListReply _defaultInstance;
  static void $checkItem(ListReply v) {
    if (v is! ListReply) checkItemFailed(v, 'ListReply');
  }

  List<Session> get sessions => $_getList(0);
}

class _ReadonlyListReply extends ListReply with ReadonlyMessageMixin {}

class LeaveRequest extends GeneratedMessage {
  static final BuilderInfo _i = new BuilderInfo('LeaveRequest')
    ..aOS(1, 'sessionId')
    ..hasRequiredFields = false
  ;

  LeaveRequest() : super();
  LeaveRequest.fromBuffer(List<int> i, [ExtensionRegistry r = ExtensionRegistry.EMPTY]) : super.fromBuffer(i, r);
  LeaveRequest.fromJson(String i, [ExtensionRegistry r = ExtensionRegistry.EMPTY]) : super.fromJson(i, r);
  LeaveRequest clone() => new LeaveRequest()..mergeFromMessage(this);
  BuilderInfo get info_ => _i;
  static LeaveRequest create() => new LeaveRequest();
  static PbList<LeaveRequest> createRepeated() => new PbList<LeaveRequest>();
  static LeaveRequest getDefault() {
    if (_defaultInstance == null) _defaultInstance = new _ReadonlyLeaveRequest();
    return _defaultInstance;
  }
  static LeaveRequest _defaultInstance;
  static void $checkItem(LeaveRequest v) {
    if (v is! LeaveRequest) checkItemFailed(v, 'LeaveRequest');
  }

  String get sessionId => $_getS(0, '');
  set sessionId(String v) { $_setString(0, v); }
  bool hasSessionId() => $_has(0);
  void clearSessionId() => clearField(1);
}

class _ReadonlyLeaveRequest extends LeaveRequest with ReadonlyMessageMixin {}

class LeaveReply extends GeneratedMessage {
  static final BuilderInfo _i = new BuilderInfo('LeaveReply')
    ..aOB(1, 'success')
    ..hasRequiredFields = false
  ;

  LeaveReply() : super();
  LeaveReply.fromBuffer(List<int> i, [ExtensionRegistry r = ExtensionRegistry.EMPTY]) : super.fromBuffer(i, r);
  LeaveReply.fromJson(String i, [ExtensionRegistry r = ExtensionRegistry.EMPTY]) : super.fromJson(i, r);
  LeaveReply clone() => new LeaveReply()..mergeFromMessage(this);
  BuilderInfo get info_ => _i;
  static LeaveReply create() => new LeaveReply();
  static PbList<LeaveReply> createRepeated() => new PbList<LeaveReply>();
  static LeaveReply getDefault() {
    if (_defaultInstance == null) _defaultInstance = new _ReadonlyLeaveReply();
    return _defaultInstance;
  }
  static LeaveReply _defaultInstance;
  static void $checkItem(LeaveReply v) {
    if (v is! LeaveReply) checkItemFailed(v, 'LeaveReply');
  }

  bool get success => $_get(0, false);
  set success(bool v) { $_setBool(0, v); }
  bool hasSuccess() => $_has(0);
  void clearSuccess() => clearField(1);
}

class _ReadonlyLeaveReply extends LeaveReply with ReadonlyMessageMixin {}

class SetMaxPlayers extends GeneratedMessage {
  static final BuilderInfo _i = new BuilderInfo('SetMaxPlayers')
    ..a<int>(1, 'number', PbFieldType.OU3)
    ..hasRequiredFields = false
  ;

  SetMaxPlayers() : super();
  SetMaxPlayers.fromBuffer(List<int> i, [ExtensionRegistry r = ExtensionRegistry.EMPTY]) : super.fromBuffer(i, r);
  SetMaxPlayers.fromJson(String i, [ExtensionRegistry r = ExtensionRegistry.EMPTY]) : super.fromJson(i, r);
  SetMaxPlayers clone() => new SetMaxPlayers()..mergeFromMessage(this);
  BuilderInfo get info_ => _i;
  static SetMaxPlayers create() => new SetMaxPlayers();
  static PbList<SetMaxPlayers> createRepeated() => new PbList<SetMaxPlayers>();
  static SetMaxPlayers getDefault() {
    if (_defaultInstance == null) _defaultInstance = new _ReadonlySetMaxPlayers();
    return _defaultInstance;
  }
  static SetMaxPlayers _defaultInstance;
  static void $checkItem(SetMaxPlayers v) {
    if (v is! SetMaxPlayers) checkItemFailed(v, 'SetMaxPlayers');
  }

  int get number => $_get(0, 0);
  set number(int v) { $_setUnsignedInt32(0, v); }
  bool hasNumber() => $_has(0);
  void clearNumber() => clearField(1);
}

class _ReadonlySetMaxPlayers extends SetMaxPlayers with ReadonlyMessageMixin {}

class JoinRequest extends GeneratedMessage {
  static final BuilderInfo _i = new BuilderInfo('JoinRequest')
    ..aOS(1, 'sessionId')
    ..hasRequiredFields = false
  ;

  JoinRequest() : super();
  JoinRequest.fromBuffer(List<int> i, [ExtensionRegistry r = ExtensionRegistry.EMPTY]) : super.fromBuffer(i, r);
  JoinRequest.fromJson(String i, [ExtensionRegistry r = ExtensionRegistry.EMPTY]) : super.fromJson(i, r);
  JoinRequest clone() => new JoinRequest()..mergeFromMessage(this);
  BuilderInfo get info_ => _i;
  static JoinRequest create() => new JoinRequest();
  static PbList<JoinRequest> createRepeated() => new PbList<JoinRequest>();
  static JoinRequest getDefault() {
    if (_defaultInstance == null) _defaultInstance = new _ReadonlyJoinRequest();
    return _defaultInstance;
  }
  static JoinRequest _defaultInstance;
  static void $checkItem(JoinRequest v) {
    if (v is! JoinRequest) checkItemFailed(v, 'JoinRequest');
  }

  String get sessionId => $_getS(0, '');
  set sessionId(String v) { $_setString(0, v); }
  bool hasSessionId() => $_has(0);
  void clearSessionId() => clearField(1);
}

class _ReadonlyJoinRequest extends JoinRequest with ReadonlyMessageMixin {}

class Session extends GeneratedMessage {
  static final BuilderInfo _i = new BuilderInfo('Session')
    ..aOS(1, 'sessionId')
    ..aOS(2, 'name')
    ..hasRequiredFields = false
  ;

  Session() : super();
  Session.fromBuffer(List<int> i, [ExtensionRegistry r = ExtensionRegistry.EMPTY]) : super.fromBuffer(i, r);
  Session.fromJson(String i, [ExtensionRegistry r = ExtensionRegistry.EMPTY]) : super.fromJson(i, r);
  Session clone() => new Session()..mergeFromMessage(this);
  BuilderInfo get info_ => _i;
  static Session create() => new Session();
  static PbList<Session> createRepeated() => new PbList<Session>();
  static Session getDefault() {
    if (_defaultInstance == null) _defaultInstance = new _ReadonlySession();
    return _defaultInstance;
  }
  static Session _defaultInstance;
  static void $checkItem(Session v) {
    if (v is! Session) checkItemFailed(v, 'Session');
  }

  String get sessionId => $_getS(0, '');
  set sessionId(String v) { $_setString(0, v); }
  bool hasSessionId() => $_has(0);
  void clearSessionId() => clearField(1);

  String get name => $_getS(1, '');
  set name(String v) { $_setString(1, v); }
  bool hasName() => $_has(1);
  void clearName() => clearField(2);
}

class _ReadonlySession extends Session with ReadonlyMessageMixin {}

