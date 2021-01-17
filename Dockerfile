FROM continuumio/miniconda3
WORKDIR /sentianaly
# Create the environment:
COPY environment.yml .
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]
RUN python -c "import mlxtend"
# The code to run when container is started:
COPY . /sentianaly
ENTRYPOINT ["conda", "run", "-n", "myenv", "python", "run.py"]
