activate:
	source run.sh; activate

install:
	source run.sh; install

run:
	source run.sh; run $(port)

create-logs-folder:
	if [ -d "logs" ]; \
	then echo "The logs folder existed"; \
	else echo "The log folder doesn't exist"; \
	mkdir logs; \
	echo "The log folder was created"; \
	fi

docker-up:
	source run.sh; docker_up
	docker exec -it -d python-flask-songs-api make run-docker

docker-down:
	source run.sh; docker_down

run-docker:
ifeq ($(strip $(port)),)
	flask run -h 0.0.0.0
else
	flask run -p $(port) -h 0.0.0.0
endif

run-worker:
ifeq ($(strip $(queue)),)
	echo "Error: You should pass the queue param"
else
	celery -A tasks.tasks worker -l info -Q $(queue)
endif

run-flask-broker:
	make create-logs-folder
ifeq ($(strip $(port)),)
	make run-worker queue=logs; flask run
else
	make run-worker queue=logs; flask run -p $(port)
endif

run-flask-broker-docker:
	make create-logs-folder
ifeq ($(strip $(port)),)
	make run-worker queue=logs; flask run -h 0.0.0.0
else
	make run-worker queue=logs; flask run -p $(port) -h 0.0.0.0
endif

docker-redis-up:
	docker compose -f docker-compose.redis.yml up --build -d

docker-redis-down:
	docker compose -f docker-compose.redis.yml down