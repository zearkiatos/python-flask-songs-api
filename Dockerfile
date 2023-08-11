FROM python:alpine3.11

COPY . /app/

WORKDIR /app

RUN apk add g++ jpeg-dev zlib-dev libjpeg make
RUN apk add libffi-dev
RUN make activate
RUN make install

EXPOSE 5000

ENTRYPOINT [ "python" ]

RUN make run