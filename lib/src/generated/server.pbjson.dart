///
//  Generated code. Do not modify.
///
// ignore_for_file: non_constant_identifier_names,library_prefixes
library server_server_pbjson;

const newSession$json = const {
  '1': 'newSession',
  '2': const [
    const {'1': 'name', '3': 1, '4': 1, '5': 9, '10': 'name'},
  ],
};

const ListRequest$json = const {
  '1': 'ListRequest',
  '2': const [
    const {'1': 'limit', '3': 1, '4': 1, '5': 13, '10': 'limit'},
  ],
};

const ListReply$json = const {
  '1': 'ListReply',
  '2': const [
    const {'1': 'sessions', '3': 1, '4': 3, '5': 11, '6': '.server.Session', '10': 'sessions'},
  ],
};

const LeaveRequest$json = const {
  '1': 'LeaveRequest',
  '2': const [
    const {'1': 'sessionId', '3': 1, '4': 1, '5': 9, '10': 'sessionId'},
  ],
};

const LeaveReply$json = const {
  '1': 'LeaveReply',
  '2': const [
    const {'1': 'success', '3': 1, '4': 1, '5': 8, '10': 'success'},
  ],
};

const SetMaxPlayers$json = const {
  '1': 'SetMaxPlayers',
  '2': const [
    const {'1': 'number', '3': 1, '4': 1, '5': 13, '10': 'number'},
  ],
};

const JoinRequest$json = const {
  '1': 'JoinRequest',
  '2': const [
    const {'1': 'sessionId', '3': 1, '4': 1, '5': 9, '10': 'sessionId'},
  ],
};

const Session$json = const {
  '1': 'Session',
  '2': const [
    const {'1': 'sessionId', '3': 1, '4': 1, '5': 9, '10': 'sessionId'},
    const {'1': 'name', '3': 2, '4': 1, '5': 9, '10': 'name'},
  ],
};

