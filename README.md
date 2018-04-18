# COS301-DND-Backend
[![Build Status](https://travis-ci.org/COS301-OptimizePrime/COS301_DND_Backend.svg?branch=develop)](https://travis-ci.org/COS301-OptimizePrime/COS301_DND_Backend)

Backed API Server

The implementation of the API uses gRPC (https://grpc.io/)

The API "Language" uses ProtocolBuffers
https://developers.google.com/protocol-buffers/docs/proto3

## Generating code from protobuffers

```bash
python -m grpc.tools.protoc -I./protos --python_out=./server --grpc_python_out=./server ./protos/server.proto
```