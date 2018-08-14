.PHONY: test run install upload clean bootstrap benchmark generate
test:
	cd ./test; echo "===Runing python tests!==="; sh -c 'pytest'

run:
	rm dnd_backend.db dnd_backend.log dnd_backend.err; export ENV=dev; sh -c 'python3 ./main.py'

prod:
	export ENV=prod; sh -c 'pypy3 ./main.py'

install:
	npm install
	pip install --upgrade -r requirements.txt

install_dev:
	cd ./test; pub get
	npm install
	python3 -m pip install --upgrade --user -r requirements.txt

install_prod:
	pypy3 -m pip install --upgrade --user -r requirements.txt

generate:
	python -m grpc.tools.protoc -I./protos --python_out=./server --grpc_python_out=./server ./protos/server.proto
	cp ./server/server_pb2.py ./test/server_pb2.py
	cp ./server/server_pb2_grpc.py ./test/server_pb2_grpc.py
	protoc -I protos/ protos/server.proto --dart_out=grpc:test/lib/

benchmark:
	cd ./test; echo "===Runing python tests!==="; sh -c 'pytest test_sessions.py --benchmark-autosave --benchmark-compare --benchmark-histogram'; sh -c 'pytest test_characters.py';
