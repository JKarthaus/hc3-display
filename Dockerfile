FROM seblucas/alpine-python3

WORKDIR /usr/src/app

RUN apk add make gcc python3-dev libc-dev linux-headers

RUN pip install --no-cache-dir pika smbus

COPY *.py ./ 

CMD [ "python3", "./lcdDisplay.py" ]
