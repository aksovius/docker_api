FROM python:slim-buster
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip \
    pip install --no-cache-dir -r /app/requirements.txt
COPY app app
WORKDIR /app