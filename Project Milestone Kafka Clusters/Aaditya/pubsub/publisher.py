from google.cloud import pubsub_v1
import os

credentials_path = "/Users/Aadi/Downloads/smartmeter gcp priviate key.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

publisher = pubsub_v1.PublisherClient()
topic_path = "projects/cloud-computing-375821/topics/smartMeter"

data = "Pub sub is working"
data = data.encode("utf-8")

future = publisher.publish(topic_path, data)
print(f"published message id{future.result()}")
