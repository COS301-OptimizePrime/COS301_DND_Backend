///
//  Generated code. Do not modify.
///
// ignore_for_file: non_constant_identifier_names,library_prefixes
library session_server;

// ignore: UNUSED_SHOWN_NAME
import 'dart:core' show int, bool, double, String, List, override;

import 'package:fixnum/fixnum.dart';
import 'package:protobuf/protobuf.dart';

class GetSessionRequest extends GeneratedMessage {
  static final BuilderInfo _i = new BuilderInfo('GetSessionRequest')
    ..aOS(1, 'authIdToken')
    ..aOS(2, 'sessionId')
    ..hasRequiredFields = false
  ;

  GetSessionRequest() : super();
  GetSessionRequest.fromBuffer(List<int> i, [ExtensionRegistry r = ExtensionRegistry.EMPTY]) : super.fromBuffer(i, r);
  GetSessionRequest.fromJson(String i, [ExtensionRegistry r = ExtensionRegistry.EMPTY]) : super.fromJson(i, r);
  GetSessionRequest clone() => new GetSessionRequest()..mergeFromMessage(this);
  BuilderInfo get info_ => _i;
  static GetSessionRequest create() => new GetSessionRequest();
  static PbList<GetSessionRequest> createRepeated() => new PbList<GetSessionRequest>();
  static GetSessionRequest getDefault() {
    if (_defaultInstance == null) _defaultInstance = new _ReadonlyGetSessionRequest();
    return _defaultInstance;
  }
  static GetSessionRequest _defaultInstance;
  static void $checkItem(GetSessionRequest v) {
    if (v is! GetSessionRequest) checkItemFailed(v, 'GetSessionRequest');
  }

  String get authIdToken => $_getS(0, '');
  set authIdToken(String v) { $_setString(0, v); }
  bool hasAuthIdToken() => $_has(0);
  void clearAuthIdToken() => clearField(1);

  String get sessionId => $_getS(1, '');
  set sessionId(String v) { $_setString(1, v); }
  bool hasSessionId() => $_has(1);
  void clearSessionId() => clearField(2);
}

class _ReadonlyGetSessionRequest extends GetSessionRequest with ReadonlyMessageMixin {}

class NewSessionRequest extends GeneratedMessage {
  static final BuilderInfo _i = new BuilderInfo('NewSessionRequest')
    ..aOS(1, 'authIdToken')
    ..aOS(2, 'name')
    ..hasRequiredFields = false
  ;

  NewSessionRequest() : super();
  NewSessionRequest.fromBuffer(List<int> i, [ExtensionRegistry r = ExtensionRegistry.EMPTY]) : super.fromBuffer(i, r);
  NewSessionRequest.fromJson(String i, [ExtensionRegistry r = ExtensionRegistry.EMPTY]) : super.fromJson(i, r);
  NewSessionRequest clone() => new NewSessionRequest()..mergeFromMessage(this);
  BuilderInfo get info_ => _i;
  static NewSessionRequest create() => new NewSessionRequest();
  static PbList<NewSessionRequest> createRepeated() => new PbList<NewSessionRequest>();
  static NewSessionRequest getDefault() {
    if (_defaultInstance == null) _defaultInstance = new _ReadonlyNewSessionRequest();
    return _defaultInstance;
  }
  static NewSessionRequest _defaultInstance;
  static void $checkItem(NewSessionRequest v) {
    if (v is! NewSessionRequest) checkItemFailed(v, 'NewSessionRequest');
  }

  String get authIdToken => $_getS(0, '');
  set authIdToken(String v) { $_setString(0, v); }
  bool hasAuthIdToken() => $_has(0);
  void clearAuthIdToken() => clearField(1);

  String get name => $_getS(1, '');
  set name(String v) { $_setString(1, v); }
  bool hasName() => $_has(1);
  void clearName() => clearField(2);
}

class _ReadonlyNewSessionRequest extends NewSessionRequest with ReadonlyMessageMixin {}

class ListRequest extends GeneratedMessage {
  static final BuilderInfo _i = new BuilderInfo('ListRequest')
    ..aOS(1, 'authIdToken')
    ..a<int>(2, 'limit', PbFieldType.OU3)
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

  String get authIdToken => $_getS(0, '');
  set authIdToken(String v) { $_setString(0, v); }
  bool hasAuthIdToken() => $_has(0);
  void clearAuthIdToken() => clearField(1);

  int get limit => $_get(1, 0);
  set limit(int v) { $_setUnsignedInt32(1, v); }
  bool hasLimit() => $_has(1);
  void clearLimit() => clearField(2);
}

class _ReadonlyListRequest extends ListRequest with ReadonlyMessageMixin {}

class LeaveRequest extends GeneratedMessage {
  static final BuilderInfo _i = new BuilderInfo('LeaveRequest')
    ..aOS(1, 'authIdToken')
    ..aOS(2, 'sessionId')
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

  String get authIdToken => $_getS(0, '');
  set authIdToken(String v) { $_setString(0, v); }
  bool hasAuthIdToken() => $_has(0);
  void clearAuthIdToken() => clearField(1);

  String get sessionId => $_getS(1, '');
  set sessionId(String v) { $_setString(1, v); }
  bool hasSessionId() => $_has(1);
  void clearSessionId() => clearField(2);
}

class _ReadonlyLeaveRequest extends LeaveRequest with ReadonlyMessageMixin {}

class JoinRequest extends GeneratedMessage {
  static final BuilderInfo _i = new BuilderInfo('JoinRequest')
    ..aOS(1, 'authIdToken')
    ..aOS(2, 'sessionId')
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

  String get authIdToken => $_getS(0, '');
  set authIdToken(String v) { $_setString(0, v); }
  bool hasAuthIdToken() => $_has(0);
  void clearAuthIdToken() => clearField(1);

  String get sessionId => $_getS(1, '');
  set sessionId(String v) { $_setString(1, v); }
  bool hasSessionId() => $_has(1);
  void clearSessionId() => clearField(2);
}

class _ReadonlyJoinRequest extends JoinRequest with ReadonlyMessageMixin {}

class SetMaxPlayersRequest extends GeneratedMessage {
  static final BuilderInfo _i = new BuilderInfo('SetMaxPlayersRequest')
    ..aOS(1, 'authIdToken')
    ..a<int>(2, 'number', PbFieldType.OU3)
    ..a<Session>(3, 'session', PbFieldType.OM, Session.getDefault, Session.create)
    ..hasRequiredFields = false
  ;

  SetMaxPlayersRequest() : super();
  SetMaxPlayersRequest.fromBuffer(List<int> i, [ExtensionRegistry r = ExtensionRegistry.EMPTY]) : super.fromBuffer(i, r);
  SetMaxPlayersRequest.fromJson(String i, [ExtensionRegistry r = ExtensionRegistry.EMPTY]) : super.fromJson(i, r);
  SetMaxPlayersRequest clone() => new SetMaxPlayersRequest()..mergeFromMessage(this);
  BuilderInfo get info_ => _i;
  static SetMaxPlayersRequest create() => new SetMaxPlayersRequest();
  static PbList<SetMaxPlayersRequest> createRepeated() => new PbList<SetMaxPlayersRequest>();
  static SetMaxPlayersRequest getDefault() {
    if (_defaultInstance == null) _defaultInstance = new _ReadonlySetMaxPlayersRequest();
    return _defaultInstance;
  }
  static SetMaxPlayersRequest _defaultInstance;
  static void $checkItem(SetMaxPlayersRequest v) {
    if (v is! SetMaxPlayersRequest) checkItemFailed(v, 'SetMaxPlayersRequest');
  }

  String get authIdToken => $_getS(0, '');
  set authIdToken(String v) { $_setString(0, v); }
  bool hasAuthIdToken() => $_has(0);
  void clearAuthIdToken() => clearField(1);

  int get number => $_get(1, 0);
  set number(int v) { $_setUnsignedInt32(1, v); }
  bool hasNumber() => $_has(1);
  void clearNumber() => clearField(2);

  Session get session => $_getN(2);
  set session(Session v) { setField(3, v); }
  bool hasSession() => $_has(2);
  void clearSession() => clearField(3);
}

class _ReadonlySetMaxPlayersRequest extends SetMaxPlayersRequest with ReadonlyMessageMixin {}

class ListReply extends GeneratedMessage {
  static final BuilderInfo _i = new BuilderInfo('ListReply')
    ..pp<Session>(1, 'sessions', PbFieldType.PM, Session.$checkItem, Session.create)
    ..aOS(2, 'status')
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

  String get status => $_getS(1, '');
  set status(String v) { $_setString(1, v); }
  bool hasStatus() => $_has(1);
  void clearStatus() => clearField(2);
}

class _ReadonlyListReply extends ListReply with ReadonlyMessageMixin {}

class LeaveReply extends GeneratedMessage {
  static final BuilderInfo _i = new BuilderInfo('LeaveReply')
    ..aOB(1, 'success')
    ..aOS(2, 'status')
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

  String get status => $_getS(1, '');
  set status(String v) { $_setString(1, v); }
  bool hasStatus() => $_has(1);
  void clearStatus() => clearField(2);
}

class _ReadonlyLeaveReply extends LeaveReply with ReadonlyMessageMixin {}

class Session extends GeneratedMessage {
  static final BuilderInfo _i = new BuilderInfo('Session')
    ..aOS(1, 'status')
    ..aOS(2, 'statusMessage')
    ..aOS(3, 'sessionId')
    ..aOS(4, 'name')
    ..a<User>(5, 'dungeonMaster', PbFieldType.OM, User.getDefault, User.create)
    ..aInt64(6, 'dateCreated')
    ..a<int>(7, 'maxPlayers', PbFieldType.OU3)
    ..pp<User>(8, 'users', PbFieldType.PM, User.$checkItem, User.create)
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

  String get status => $_getS(0, '');
  set status(String v) { $_setString(0, v); }
  bool hasStatus() => $_has(0);
  void clearStatus() => clearField(1);

  String get statusMessage => $_getS(1, '');
  set statusMessage(String v) { $_setString(1, v); }
  bool hasStatusMessage() => $_has(1);
  void clearStatusMessage() => clearField(2);

  String get sessionId => $_getS(2, '');
  set sessionId(String v) { $_setString(2, v); }
  bool hasSessionId() => $_has(2);
  void clearSessionId() => clearField(3);

  String get name => $_getS(3, '');
  set name(String v) { $_setString(3, v); }
  bool hasName() => $_has(3);
  void clearName() => clearField(4);

  User get dungeonMaster => $_getN(4);
  set dungeonMaster(User v) { setField(5, v); }
  bool hasDungeonMaster() => $_has(4);
  void clearDungeonMaster() => clearField(5);

  Int64 get dateCreated => $_getI64(5);
  set dateCreated(Int64 v) { $_setInt64(5, v); }
  bool hasDateCreated() => $_has(5);
  void clearDateCreated() => clearField(6);

  int get maxPlayers => $_get(6, 0);
  set maxPlayers(int v) { $_setUnsignedInt32(6, v); }
  bool hasMaxPlayers() => $_has(6);
  void clearMaxPlayers() => clearField(7);

  List<User> get users => $_getList(7);
}

class _ReadonlySession extends Session with ReadonlyMessageMixin {}

class User extends GeneratedMessage {
  static final BuilderInfo _i = new BuilderInfo('User')
    ..aOS(1, 'uid')
    ..aOS(2, 'name')
    ..hasRequiredFields = false
  ;

  User() : super();
  User.fromBuffer(List<int> i, [ExtensionRegistry r = ExtensionRegistry.EMPTY]) : super.fromBuffer(i, r);
  User.fromJson(String i, [ExtensionRegistry r = ExtensionRegistry.EMPTY]) : super.fromJson(i, r);
  User clone() => new User()..mergeFromMessage(this);
  BuilderInfo get info_ => _i;
  static User create() => new User();
  static PbList<User> createRepeated() => new PbList<User>();
  static User getDefault() {
    if (_defaultInstance == null) _defaultInstance = new _ReadonlyUser();
    return _defaultInstance;
  }
  static User _defaultInstance;
  static void $checkItem(User v) {
    if (v is! User) checkItemFailed(v, 'User');
  }

  String get uid => $_getS(0, '');
  set uid(String v) { $_setString(0, v); }
  bool hasUid() => $_has(0);
  void clearUid() => clearField(1);

  String get name => $_getS(1, '');
  set name(String v) { $_setString(1, v); }
  bool hasName() => $_has(1);
  void clearName() => clearField(2);
}

class _ReadonlyUser extends User with ReadonlyMessageMixin {}
