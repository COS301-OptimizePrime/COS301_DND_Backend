import "package:test/test.dart";
import "package:grpc/grpc.dart";
import 'dart:io';

import 'lib/server.pb.dart';
import 'lib/server.pbgrpc.dart';

void main() {
  test("test_create_rpc_good_login", () async {
    String token= "";
    await Process.run('node', ['./login.mjs']).then((ProcessResult results) {
     token = results.stdout.trim();
    });
    //print('Token received: {${token}}');


    final channel = new ClientChannel('localhost',
      port: 50051,
      options: const ChannelOptions(
          credentials: const ChannelCredentials.insecure()));
    final stub = new SessionsManagerClient(channel);

    NewSessionRequest nsr = new NewSessionRequest();
    nsr.name = "mySession";
    nsr.authIdToken = token;
    final response = await stub.create(nsr);
    print('Client received: ${response.status}');
    expect(response.status, equals("SUCCESS"));

    await channel.shutdown();
  });
}