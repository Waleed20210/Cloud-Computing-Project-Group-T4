import os
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=""
project_id = ""
subscription_id = "smartmeter_out-sub"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received message.")
    print(f"{message.data}\n")
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

with subscriber:
        streaming_pull_future.result()  # Block until the shutdown is complete.