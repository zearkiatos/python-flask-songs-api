FROM python:alpine3.17

COPY . /app/

WORKDIR /app

RUN apk add g++ jpeg-dev zlib-dev libjpeg make gcc
RUN apk add libffi-dev
RUN pip install Cmake
RUN make install

EXPOSE 5000

ENTRYPOINT [ "python3" ]

RUN make run