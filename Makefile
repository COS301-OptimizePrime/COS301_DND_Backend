.PHONY: test run install upload clean bootstrap
test:
	cd ./test; echo "===Runing python tests!==="; sh -c 'python ./main.py'; echo "===Runing dart tests!==="; dart test.dart;

run:
	export ENV=dev; sh -c 'python ./server/main.py'

prod:
	export ENV=prod; sh -c 'python ./server/main.py'

install:
	cd ./test; pub get
	npm install
	pip install --user -r requirements.txt

generate:
	python -m grpc.tools.protoc -I./protos --python_out=./server --grpc_python_out=./server ./protos/server.proto
	cp ./server/server_pb2.py ./test/server_pb2.py
	cp ./server/server_pb2_grpc.py ./test/server_pb2_grpc.py
	protoc -I protos/ protos/server.proto --dart_out=grpc:test/lib/