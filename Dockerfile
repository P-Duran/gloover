FROM frolvlad/alpine-miniconda3

ENV GROUP_ID=1000 \
    USER_ID=1000

ENV FLASK_APP=gloover_ws/app.py
ENV FLASK_RUN_HOST=0.0.0.0

WORKDIR /var/www/

COPY . /var/www/

RUN addgroup -g $GROUP_ID www
RUN adduser -D -u $USER_ID -G www www -s /bin/sh

# Create the environment:
COPY environment.yml .
RUN conda env create -f environment.yml
# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "myenv", "/bin/sh", "-c"]
RUN python -c "import nltk"
EXPOSE 5000

# The code to run when container is started:
ENTRYPOINT ["conda", "run", "-n", "myenv", "python", "run.py"]
