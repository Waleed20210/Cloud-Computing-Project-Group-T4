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

#Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from joblib import dump, load

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from google.cloud import storage
from tempfile import TemporaryFile

class PredictDoFn(beam.DoFn):

  def setup(self):
        """
        Download sklearn model from GCS
        """
        storage_client = storage.Client("cloud-project-milestones")
        bucket = storage_client.get_bucket('cloud-project-milestones-bucket')
        blob = bucket.blob('velocityPredictor.joblib')
        blob.download_to_filename('velocityPredictor.joblib')
        # unpickle sklearn model
        self.loaded_model = load('velocityPredictor.joblib')

  def process(self, element):
    dataframe = pd.DataFrame([element], columns=element.keys())
    result = self.loaded_model.predict(dataframe)
    # element['predictedVel'] = result[0]
    predictedValue = result[0]
    element['predictedVel'] = predictedValue.item()
    # element['predictedVel'] = json.dumps(result.tolist())
    print(element)
    return [element]

def filterRcds(element):
    """
    Filter records with None value
    """
    return((element['width'] != None) and (element['height'] != None) and (element['width'] != 0) and (element['height'] != 0))

class PreprocessDataDoFn(beam.DoFn):
    """
    Preprocess and drop unused columns
    """

    def process(self, element):
        """
        Preprocess and drop unused columns
        """
        df = pd.DataFrame([element], columns=element.keys())
        df = df.drop('id', axis=1)
        df = df.drop('initialFrame', axis=1)
        df = df.drop('finalFrame', axis=1)
        df = df.drop('numFrames', axis=1)
        df = df.drop('drivingDirection', axis=1)
        df = df.drop('traveledDistance', axis=1)
        df = df.drop('minXVelocity', axis=1)
        df = df.drop('maxXVelocity', axis=1)
        df = df.drop('minDHW', axis=1)
        df = df.drop('minTHW', axis=1)
        df = df.drop('minTTC', axis=1)
        df = df.drop('numLaneChanges', axis=1)
        df = df.drop('class', axis=1)
        df = df.drop('meanXVelocity', axis=1)
        element = df.to_dict('records')
        return element


def run(argv=None):
  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('--input', dest='input', required=True,
                      help='Input file to process.')
  parser.add_argument('--output', dest='output', required=True,
                      help='Output file to write results to.')
  parser.add_argument('--model', dest='model', required=True,
                      help='Checkpoint file of the model.')
  known_args, pipeline_args = parser.parse_known_args(argv)
  pipeline_options = PipelineOptions(pipeline_args)
  pipeline_options.view_as(SetupOptions).save_main_session = True;

  with beam.Pipeline(options=pipeline_options) as p:
        track = (p | 'ReadFromBQ' >> beam.io.gcp.bigquery.ReadFromBigQuery(table=known_args.input)); # reads the table rows from Big Query and converts to a python dictionary
                    # | "toDict" >> beam.Map(lambda x: json.loads(x)));
        logging.info(type(track))

        # filterRow=(track | 'filter' >> beam.Filter(lambda x: x[0]==0 and x[0] is not None)) # filters out 0 and null values from the dataset
        filterRecords = track | 'Filter Records' >> beam.Filter(filterRcds)
        logging.info(type(filterRecords))

        preprocess = filterRecords | 'Preprocess Data' >> beam.ParDo(PreprocessDataDoFn()) # running the predictions
        logging.info(type(preprocess))

        predictions = preprocess | 'Predictions' >> beam.ParDo(PredictDoFn()) # running the predictions
        logging.info(type(predictions))

        # print(predictions)
        schema = 'width:FLOAT, height:FLOAT, predictedVel:FLOAT64'
        predictions | 'WriteToBQ' >> beam.io.gcp.bigquery.WriteToBigQuery(
            known_args.output,
            schema=schema,
            create_disposition='CREATE_IF_NEEDED') # write to big query

        (predictions | 'to byte' >> beam.Map(lambda x: json.dumps(x).encode('utf8'))
            |   'to Pub/sub' >> beam.io.WriteToPubSub("projects/cloud-project-milestones/topics/milestone2_pub")); # simultaenously publish to Pub/Sub

if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  run()