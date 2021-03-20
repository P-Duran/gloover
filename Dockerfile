FROM python:3.8-slim

ENV FLASK_APP=gloover_ws/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_DEBUG=1
ENV FLASK_PORT=5000
WORKDIR /var/www/

# Install required packages:
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install git
RUN apt-get -y install gcc
RUN pip install --upgrade pip
# intell requirements and import needed data:
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python3 -m spacy download en
RUN python3 -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('stopwords'); nltk.download('wordnet');"
#Copy all data needed from the project
COPY setup.py .
COPY resources /var/www/resources
COPY gloover_ws /var/www/gloover_ws
COPY gloover_service /var/www/gloover_service
COPY gloover_model /var/www/gloover_model
RUN ls
RUN python setup.py install

EXPOSE 5000

# The code to run when container is started:
ENTRYPOINT ["flask", "run"]


