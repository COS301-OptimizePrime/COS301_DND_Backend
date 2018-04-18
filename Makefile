.PHONY: test upload clean bootstrap
test:
	cd ./test; python main.py

run:
	sh -c 'python ./server/main.py'
