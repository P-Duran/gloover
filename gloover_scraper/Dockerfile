FROM python:3.8-slim

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_DEBUG=1
ENV FLASK_PORT=9080
WORKDIR /var/www/app

# Install required packages:
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install git
RUN apt-get -y install gcc
RUN pip install --upgrade pip
# intell requirements and import needed data:
COPY requirements.txt .
RUN pip install -r requirements.txt


COPY . .
EXPOSE 9080
# The code to run when container is started:
ENTRYPOINT ["flask", "run", "--port=9080"]


