# COS301-DND-Backend

| Branch  |                                                                               Status                                                                               |
| ------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| Master  | [![Build Status](https://travis-ci.org/COS301-OptimizePrime/COS301_DND_Backend.svg?branch=master)](https://travis-ci.org/COS301-OptimizePrime/COS301_DND_Backend)  |
| Develop | [![Build Status](https://travis-ci.org/COS301-OptimizePrime/COS301_DND_Backend.svg?branch=develop)](https://travis-ci.org/COS301-OptimizePrime/COS301_DND_Backend) ![deployment diagram](https://img.shields.io/badge/coverage-80%25-brightgreen.svg)
 |

Backed API Server

## Deployment Diagram
![deployment diagram](https://i.imgur.com/DFwdbp0.jpg)

## Features

- HTTP/2 using gRPC (https://grpc.io/)
- HTTPS in production mode
- Real time sockets
- Firebase authentication
- Strongly typed service and message definition (Protobuf3)
- Easy configuration with TOML
- pep8 Compliance
- Regression testing
- Developer mode (SQLite)
- Production mode (PostgreSQL and PyPy3)
- SystemD service file


## Coverage

|Name                          |Stmts  | Miss| Cover|
|:-----------------------------|-----:|----:|-----:|
|main.py                       | 54   |   5 |   91%|
|server/__init__.py            |  0   |   0 |  100%|
|server/character.py           |257   |  58 |   77%|
|server/config.py              | 28   |  11 |   61%|
|server/db.py                  |179   |   4 |   98%|
|server/firebase.py            |  4   |   0 |  100%|
|server/helpers.py             |181   |   1 |   99%|
|server/log.py                 | 18   |   6 |   67%|
|server/server_pb2.py          |186   |   0 |  100%|
|server/server_pb2_grpc.py     |121   |  84 |   31%|
|server/session.py             |584   | 152 |   74%|
|TOTAL                         |1612  | 321|    80%|


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
