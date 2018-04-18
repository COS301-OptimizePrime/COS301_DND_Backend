.PHONY: test upload clean bootstrap
test:
	cd ./test; python3 main.py

run:
	sh -c 'python3 ./server/main.py'
