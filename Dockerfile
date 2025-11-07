FROM python:3.11
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade setuptools pip && pip install -r requirements.txt
COPY . /code/
#Give permissions for the code dir, to write logs
RUN chgrp -R 0 /code && \
    chmod -R g=u /code
ENTRYPOINT ["python", "run.py"]
