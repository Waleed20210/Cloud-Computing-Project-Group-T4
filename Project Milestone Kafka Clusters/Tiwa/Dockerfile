FROM python:latest

RUN pip install -U ipykernel

RUN pip install --upgrade google-cloud-pubsub

WORKDIR /workspace
COPY . /workspace

CMD [ "python3", "./client.py" ]
