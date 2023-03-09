# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import argparse
import json
import logging
import os

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions

import pymysql

#Filter: Filter: Eliminate records with missing measurements (containing None)
def eliminateMissingValues(element):
    return (element['temperature'] != None and element['humidity'] != None and element['pressure'] != None)
    
#Convert: convert the pressure from kPa to psi and the temperature from Celsius to Fahrenheit
class ConvertPresTemp(beam.DoFn):

    def process(self, element):
        result = {}
        result['time'] = element['time']
        result['profile_name'] = element['profile_name']

        if "humidity" in element and element['humidity'] != None:
            result['humidity'] = element['humidity']

        if "temperature" in element and element['temperature'] != None:
            temperature = element['temperature']*1.8+32
            result['temperature'] = temperature
            
        if "pressure" in element and element['pressure'] != None:
            pressure = element['pressure']/6.895
            result['pressure'] = pressure
        
        return [result]

#to MySQL: connects to mysql database server in GKE and runs query to save data to a table           
class saveData(beam.DoFn):

    def process(self, element):
        
        #Connect to server
        mydb = pymysql.connect(
        host="34.95.47.31",
        port=3306,
        user="usr",
        password="sofe4630u",
        database="Readings"
        )

        #Perform query
        mycursor = mydb.cursor()

        sql = "INSERT INTO dataflowReadings (time, profile_name, humidity, temperature, pressure) VALUES (%s, %s, %s, %s, %s)"
        val = (element['time'], element['profile_name'], element['humidity'], element['temperature'], element['pressure'])
        mycursor.execute(sql, val)

        mydb.commit()

def run(argv=None):
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('--input', dest='input', required=True,
                      help='Input file to process.')
  parser.add_argument('--output', dest='output', required=True,
                      help='Output file to write results to.')
  known_args, pipeline_args = parser.parse_known_args(argv)
  pipeline_options = PipelineOptions(pipeline_args)
  pipeline_options.view_as(SetupOptions).save_main_session = True;
  
  with beam.Pipeline(options=pipeline_options) as p:
    readings= (p | "Read from Pub/Sub" >> beam.io.ReadFromPubSub(topic=known_args.input)
        | "toDict" >> beam.Map(lambda x: json.loads(x)));
    
    filtered = readings | 'Filter' >> beam.Filter(eliminateMissingValues)

    conversions = filtered | 'Convert' >> beam.ParDo(ConvertPresTemp())

    (conversions | 'to bytes' >> beam.Map(lambda x: json.dumps(x).encode('utf8'))
        |   'to Pub/Sub' >> beam.io.WriteToPubSub(topic=known_args.output));

    (conversions | 'to MySQL' >> beam.ParDo(saveData()));
        
if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  run()