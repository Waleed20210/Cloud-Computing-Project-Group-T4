# from confluent_kafka import Producer, KafkaError
import json
import time
import random
import numpy as np
from google.cloud import pubsub_v1
import os
import logging


import argparse
import apache_beam as beam

from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions

# Read arguments and configurations and initialize
# producer_conf = json.load(open('cred.json'))
# producer = Producer(producer_conf)
# topic= "<topicname>"

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cloud-project-milestones-e39a7bfc5e67.json"
# project_id = "cloud-project-milestones"
# topic_id = "projects/cloud-project-milestones/topics/milestone2_pub"

# publisher = pubsub_v1.PublisherClient()
# The `topic_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/topics/{topic_id}`
# topic_path = publisher.topic_path(project_id, topic_id)

# device normal distributions profile used to generate random data
DEVICE_PROFILES = {
    "boston": {'temp': (51.3, 17.7), 'humd': (77.4, 18.7), 'pres': (1.019, 0.091)},
    "denver": {'temp': (49.5, 19.3), 'humd': (33.0, 13.9), 'pres': (1.512, 0.341)},
    "losang": {'temp': (63.9, 11.7), 'humd': (62.8, 21.8), 'pres': (1.215, 0.201)},
}
profileNames = ["boston", "denver", "losang"]

# Optional per-message on_delivery handler (triggered by poll() or flush())
# when a message has been successfully delivered or
# permanently failed delivery (after retries).


def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: {}".format(err))
    else:
        print("Produced record to topic {} partition [{}] @ offset {}"
              .format(msg.topic(), msg.partition(), msg.offset()))


record_key = 0


# class FilterMeasurementsDoFn(beam.DoFn):
#     """
#     Filters the msg from Pub/Sub
#     """

#     def process(self,element):
#         # randomly eliminate some measurements
#         for i in range(3):
#             if(random.randrange(0, 10) < 1):
#                 choice = random.randrange(0, 3)
#                 if(choice == 0):
#                     element['temperature'] = None
#                 elif (choice == 1):
#                     element['humidity'] = None
#                 else:
#                     element['pressure'] = None
#         return element

def filterRcds(element):
    """
    Filter records with None value
    """
    return((element['temperature'] != None) and (element['humidity'] != None) and (element['pressure'] != None))
    # if((element['temperature'] != None) and (element['humidity'] != None) and (element['pressure'] != None)):
    #     return element

class ConvertMeasurementsDoFn(beam.DoFn):
    """
    Converts measurements to their respective values
    """

    def process(self, element):
        result = {}
        result['time'] = element['time']
        result['profile_name'] = element['profile_name']

        if "humidity" in element:
            result['humidity'] = element['humidity']

        if "temperature" in element:
            temperature = element['temperature']*1.8+32
            result['temperature'] = temperature
            
        if "pressure" in element:
            pressure = element['pressure']/6.895
            result['pressure'] = pressure
        
        return [result]
        # print("Element: ",element)
        # temp = convertTemp(element["temperature"])
        # pressure = convertPressure(element["pressure"])
        
        # print("Temp:",temp,"Pressure: ",pressure,sep=", ")

        # element["temperature"]=temp
        # element["pressure"]=pressure
        # return element


def convertPressure(kPa):
    """
    Converts kPa to psi
    """
    psi = kPa / 6.895
    print(psi)
    return psi


def convertTemp(celcius):
    """
    Converts Celcius to Fahrenheit
    """
    fahrenheit = (celcius * 1.8) + 32
    return fahrenheit


def run(argv=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--input', dest='input', required=True,
                        help='Input file to process.')
    parser.add_argument('--output', dest='output', required=True,
                        help='Output file to write results to.')
    # parser.add_argument('--model', dest='model', required=True,
    #                     help='Checkpoint file of the model.')
    known_args, pipeline_args = parser.parse_known_args(argv)
    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = True

    with beam.Pipeline(options=pipeline_options) as p:
        payload = (p | "Read from Pub/Sub" >> beam.io.ReadFromPubSub(topic=known_args.input)
                   | "toDict" >> beam.Map(lambda x: json.loads(x)))

        # filterRecords = payload | 'Filter Records' >> beam.ParDo(FilterMeasurementsDoFn())
        filterRecords = payload | 'Filter Records' >> beam.Filter(filterRcds)

        convertRecords = filterRecords | 'Convert Records' >> beam.ParDo(ConvertMeasurementsDoFn())

        (convertRecords | 'to byte' >> beam.Map(lambda x: json.dumps(x).encode('utf8'))
            | 'to Pub/sub' >> beam.io.WriteToPubSub(topic=known_args.output))


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
