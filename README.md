# COS301-DND-Backend
[![Build Status](https://travis-ci.org/COS301-OptimizePrime/COS301_DND_Backend.svg?branch=develop)](https://travis-ci.org/COS301-OptimizePrime/COS301_DND_Backend)

Backed API Server

The implementation of the API uses gRPC (https://grpc.io/)

The API "Language" uses ProtocolBuffers
https://developers.google.com/protocol-buffers/docs/proto3

## Requirements
```bash
sudo apt-get update
sudo apt-get install python3
sudo apt-get install pip3
sudo apt-get install nodejs
sudo apt-get install dart
```

## Installing packages
```bash
make install
```

## Running server
```bash
make run
```

## Running the tests
```bash
make test
```

## Generating code from protobuffers

```bash
python -m grpc.tools.protoc -I./protos --python_out=./server --grpc_python_out=./server ./protos/server.proto
```