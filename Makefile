.PHONY: test upload clean bootstrap
test:
	sh -c 'python3 ./test/main.py'

run:
	sh -c 'python3 ./server/main.py'
