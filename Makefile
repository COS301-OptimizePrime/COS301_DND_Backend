.PHONY: test upload clean bootstrap
test:
	sh -c 'python ./test/main.py'

run:
	sh -c 'python ./server/main.py'
