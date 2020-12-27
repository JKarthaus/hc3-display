FROM python:3.8-alpine

WORKDIR /usr/src/app

RUN apk add make gcc python3-dev libc-dev linux-headers

RUN pip install --no-cache-dir pika smbus

COPY *.py ./ 

CMD [ "python3", "./lcdDisplay.py" ]
