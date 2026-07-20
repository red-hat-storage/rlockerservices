FROM python:3.12
ENV PYTHONUNBUFFERED 1
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade --no-cache-dir setuptools pip wheel && pip install -r requirements.txt
COPY . /code/
#Give permissions for the code dir, to write logs
RUN chgrp -R 0 /code && \
    chmod -R g=u /code
ENTRYPOINT ["python", "run.py"]
