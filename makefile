activate:
	source run.sh; activate

install:
	source run.sh; install

run:
	source run.sh; run $(port)

docker-up:
	source run.sh; docker_up

docker-down:
	source run.sh; docker_down