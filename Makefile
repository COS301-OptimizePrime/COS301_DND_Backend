.PHONY: test upload clean bootstrap
test:
	cd ./test; sh -c 'python ./main.py'

run:
	sh -c 'python ./server/main.py'
