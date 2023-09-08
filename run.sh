#!/bin/bash
activate () {
    if [ -d "venv" ] 
    then
        echo "Python 🐍 environment was activated"
        source venv/bin/activate
    else
        echo "The folder environment doesn't exist"
        python3 -m venv venv
        source venv/bin/activate
        echo "The environment folder was created and the python 🐍 environment was activated"
    fi
}

install () {
    pip install -r requirements.txt
}

run () {
    cd flaskr
    if [ -z "$1" ]
    then
        flask run
    else
        flask run -p $1
    fi
}

create_logs_folder() {
    if [ -d "logs" ]
	then
        echo "The logs folder existed"
	else 
        echo "The log folder doesn't exist"
	    mkdir logs
	    echo "The log folder was created"
	fi
}

docker_up() {
    docker compose up --build -d
    docker exec -it -d python-flask-songs-api make run-docker
}

docker_down() {
    docker compose down
}

run_docker () {
    if [ -z "$1" ]
    then
        flask run -h localhost
    else
        flask run -p $1 -h localhost
    fi
}

run_worker() {
    if [ -z "$1" ]
    then
       	echo "Error: You should pass the queue param"
    else
        celery -A tasks.tasks worker -l info -Q $1
    fi
}

run_flask_broker() {
    create_logs_folder
    if [ -z "$1" ]
    then
        run_worker logs; flask run
    else
        run_worker logs; flask run -p $1
    fi
}

run_flask_broker_docker() {
    create_logs_folder
    if [ -z "$1" ]
    then
        run_worker logs; flask run -h 0.0.0.0
    else
        run_worker logs; flask run -p $1 -h 0.0.0.0
    fi
}

docker_redis_up() {
    docker compose -f docker-compose.redis.yml up --build -d
}

docker_redis_down() {
    docker compose -f docker-compose.redis.yml down
}
