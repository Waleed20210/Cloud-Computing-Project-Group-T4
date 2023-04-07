from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
import os

# TODO(developer)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="cloud-project-milestones-e39a7bfc5e67.json"
project_id = "cloud-project-milestones"
subscription_id = "milestone2_pub-sub"
# Number of seconds the subscriber should listen for messages
timeout = 5.0

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(message)
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

# Wrap subscriber in a 'with' block to automatically cal     close() when done.
with subscriber:
    streaming_pull_future.result()
    # try:
    #     # When `timeout` is not set, result() will block indefinitely,
    #     # unless an exception is encountered first.
    #     streaming_pull_future.result(timeout=timeout)
    # except TimeoutError:
    #     streaming_pull_future.cancel()  # Trigger the shutdown.
    #     streaming_pull_future.result()  # Block until the shutdown is complete.