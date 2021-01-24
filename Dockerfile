FROM continuumio/miniconda3
WORKDIR /sentianaly
# Create the environment:
COPY environment.yml .
RUN conda env create -f environment.yml
# Flask app
ENV FLASK_APP=src/server/app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]
RUN python -c "import redis"
EXPOSE 5000
# The code to run when container is started:
COPY . /sentianaly
ENTRYPOINT ["conda", "run", "-n", "myenv", "python", "run.py"]
