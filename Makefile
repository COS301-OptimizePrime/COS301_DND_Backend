.PHONY: test run install upload clean bootstrap
test:
	cd ./test; sh -c 'python ./main.py'; dart test.dart;

run:
	sh -c 'python ./server/main.py'

install:
	cd ./test; pub get
	npm install
	pip install --user -r requirements.txt