from google.cloud import pubsub_v1
import time
import numpy as np
import random
import os
import json


# TODO(developer)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="cloud-project-milestones-e39a7bfc5e67.json"
project_id = "cloud-project-milestones"
topic_id = "milestone2_pub"

publisher = pubsub_v1.PublisherClient()
# The `topic_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/topics/{topic_id}`
topic_path = publisher.topic_path(project_id, topic_id)


#device normal distributions profile used to generate random data
DEVICE_PROFILES = {
	"boston": {'temp': (51.3, 17.7), 'humd': (77.4, 18.7), 'pres': (1.019, 0.091) },
	"denver": {'temp': (49.5, 19.3), 'humd': (33.0, 13.9), 'pres': (1.512, 0.341) },
	"losang": {'temp': (63.9, 11.7), 'humd': (62.8, 21.8), 'pres': (1.215, 0.201) },
}
profileNames=["boston","denver","losang"]

# Optional per-message on_delivery handler (triggered by poll() or flush())
# when a message has been successfully delivered or
# permanently failed delivery (after retries).
def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: {}".format(err))
    else:
        print("Produced record to topic {} partition [{}] @ offset {}"
              .format(msg.topic(), msg.partition(), msg.offset()))

record_key=0
while(True):
    try:    
        profile_name = profileNames[random.randint(0, 2)]
        profile = DEVICE_PROFILES[profile_name]
        # get random values within a normal distribution of the value
        temp = max(0, np.random.normal(profile['temp'][0], profile['temp'][1]))
        humd = max(0, min(np.random.normal(profile['humd'][0], profile['humd'][1]), 100))
        pres = max(0, np.random.normal(profile['pres'][0], profile['pres'][1]))
        
        # create dictionary
        msg={"time": time.time(), "profile_name": profile_name, "temperature": temp,"humidity": humd, "pressure":pres}
        
        # #randomly eliminate some measurements
        for i in range(3):
            if(random.randrange(0,10)<1):
                choice=random.randrange(0,3)
                if(choice==0):
                    msg['temperature']=None;
                elif (choice==1):
                    msg['humidity']=None;
                else:
                    msg['pressure']=None;
                   
        # data_str = f"{msg}"
        print(msg)
        # Data must be a bytestring
        data = json.dumps(msg).encode("utf-8")
        # When you publish a message, the client returns a future.
        future = publisher.publish(topic_path, data)
        print(future.result())
    except KeyboardInterrupt:
        break
print(f"Published messages to {topic_path}.")