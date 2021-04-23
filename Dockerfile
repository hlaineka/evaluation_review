FROM debian:10-slim

RUN apt update && apt -y install python3 python3-dev python3-pip
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

RUN useradd --create-home --shell /bin/bash user
RUN adduser user sudo

COPY . .

EXPOSE 6660

ADD . /app
WORKDIR /app

CMD [ "python3", "src/main.py" ]