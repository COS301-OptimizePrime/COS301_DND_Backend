.PHONY: test run install upload clean bootstrap benchmark generate
test:
	cd ./test; echo "===Runing python tests!==="; sh -c 'pytest test_sessions.py'; sh -c 'pytest test_characters.py'; echo "===Runing dart tests!==="; dart test.dart;

run:
	rm dnd_backend.db dnd_backend.log config.toml; export ENV=dev; sh -c 'python ./main.py'

prod:
	export ENV=prod; sh -c 'pypy3 ./server/main.py'

install:
	cd ./test; pub get
	npm install
	pip install --upgrade --user -r requirements.txt

install_prod:
	cd ./test; pub get
	npm install
	pypy3 -m pip install --upgrade --user -r requirements.txt

generate:
	python -m grpc.tools.protoc -I./protos --python_out=./server --grpc_python_out=./server ./protos/server.proto
	cp ./server/server_pb2.py ./test/server_pb2.py
	cp ./server/server_pb2_grpc.py ./test/server_pb2_grpc.py
	protoc -I protos/ protos/server.proto --dart_out=grpc:test/lib/

benchmark:
	cd ./test; echo "===Runing python tests!==="; sh -c 'pytest test_sessions.py --benchmark-autosave --benchmark-compare --benchmark-histogram'; sh -c 'pytest test_characters.py';
