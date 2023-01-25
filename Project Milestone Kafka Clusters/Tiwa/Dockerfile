FROM python:latest

WORKDIR /workspace
COPY . /workspace

RUN pip install -U ipykernel
RUN pip install --upgrade google-cloud-pubsub
RUN pip install numpy
RUN pip install -r kafka/v1/requirements.txt
