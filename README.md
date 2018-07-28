# COS301-DND-Backend

| Branch  |                                                                               Status                                                                               |
| ------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| Master  | [![Build Status](https://travis-ci.org/COS301-OptimizePrime/COS301_DND_Backend.svg?branch=master)](https://travis-ci.org/COS301-OptimizePrime/COS301_DND_Backend)  ![deployment diagram](https://img.shields.io/badge/coverage-82%25-brightgreen.svg)|
| Develop | [![Build Status](https://travis-ci.org/COS301-OptimizePrime/COS301_DND_Backend.svg?branch=develop)](https://travis-ci.org/COS301-OptimizePrime/COS301_DND_Backend) ![deployment diagram](https://img.shields.io/badge/coverage-82%25-brightgreen.svg) |

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
|main.py                 |  50    |  5   | 90%|
|server/character.py     | 281    | 73   | 74%|
|server/db.py            | 167    |  3   | 98%|
|server/firebase.py      |   4    |  0   |100%|
|server/helpers.py       | 181    |  1   | 99%|
|server/log.py           |  18    |  0   |100%|
|server/server_pb2.py    | 186    |  0   |100%|
|server/session.py       | 643    |200   | 69%|
|TOTAL                   |1530    |282   | 82%|


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

## Fedora Installation
```bash
sudo dnf update
sudo dnf install postgresql-server postgresql-contrib
sudo systemctl enable postgresql
sudo postgresql-setup --initdb --unit postgresql
sudo systemctl start postgresql
pypy -m ensurepip
```

## Arch Linux Installation
```bash
pacman -S sudo
sudo pacaman -Syyu
sudo pacman -S postgresql

sudo -u postgres -i
initdb --locale en_US.UTF-8 -E UTF8 -D '/var/lib/postgres/data'
exit

sudo systemctl enable postgresql
sudo systemctl start postgresql
sudo -u postgres -i

createuser --interactive
```