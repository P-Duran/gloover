FROM python:3.8-slim


ENV GROUP_ID=1000 \
    USER_ID=1000

ENV FLASK_APP=gloover_ws/app.py
ENV FLASK_RUN_HOST=0.0.0.0

WORKDIR /var/www/

# Create the environment:
COPY requirements.txt .
RUN apt-get -y update
# Upgrade already installed packages:
RUN apt-get -y upgrade
RUN apt-get -y install git
RUN pip install --upgrade pip
# Make RUN commands use the new environment:
RUN pip install -r requirements.txt
RUN python3 -m spacy download en
RUN python3 -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('stopwords')"
COPY . /var/www/
RUN python setup.py install

EXPOSE 5000

# The code to run when container is started:
ENTRYPOINT ["flask", "run"]

