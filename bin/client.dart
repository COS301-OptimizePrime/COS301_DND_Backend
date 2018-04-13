import 'dart:async';

import 'package:grpc/grpc.dart';

import '../lib/src/generated/server.pb.dart';
import '../lib/src/generated/server.pbgrpc.dart';

Future<Null> main(List<String> args) async {
  final channel = new ClientChannel('localhost',
      port: 50051,
      options: const ChannelOptions(
          credentials: const ChannelCredentials.insecure()));
  final stub = new SessionManagerClient(channel);
  final name = 'test';

  try {
    final response = await stub.create(new newSession()..name = name);
    print('client received: ${response.name}');
  } catch (e) {
    print('Caught error: $e');
  }
  await channel.shutdown();
}