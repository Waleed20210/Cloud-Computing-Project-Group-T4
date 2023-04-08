# Cloud Final Project

## Design
- Find the pipeline design/proposal [here](https://docs.google.com/document/d/1r0pLqDuQMCbqDKsQqahURGHPus3RO9M7zlsiVZ8JRU0/edit?usp=share_link)
- [Cloud Project Demo Part1 ](https://drive.google.com/file/d/1l-yf8NnBPlca9OMT5YqYcd6cTy28LFTg/view?usp=share_link)
- [Cloud Project Demo Part2 ](https://drive.google.com/file/d/1F1JJ9czU8AHLYVgC6FzjNKMN7j64o6xh/view?usp=share_link)


## How to Run(GCP required)
- Clone the repo
- Use the following script to run the project. **Note a service account with Pub/Sub access is required. Remember to enable the tools before executing the command below**
    ```bash
    python prediction.py \
        --runner DataflowRunner \
        --project $PROJECT \
        --staging_location $BUCKET/staging \
        --temp_location $BUCKET/temp \
        --input $PROJECT:Highway_Trajectory.tracks02 \ 
        --output $PROJECT:Highway_Trajectory.Predict \
        --region  northamerica-northeast2 \
        --experiment use_unsupported_python_version \
        --streaming \
        --setup ./setup.py \
        --model $BUCKET/model \
        --job_name cloud-proj-demo
    ```
    - Use the following script to populate ur environment variables. **Note they need to be updated each time a terminal session is started**
    ```bash
    PROJECT=$(gcloud config list project --format "value(core.project)") && BUCKET=gs://$PROJECT-bucket
    ```
    - In a new terminal, use the script below to run the subscriber.
        ```bash
        python subscriber_design.py
        ```

## Team - Group T4
Waleed El Alawi (100764573)<br>
Preet Patel (100708239) <br>
Tiwaloluwa Ojo (100700622)<br>
Aaditya Rajput (100622434)<br>


## Short Project Description
There are commercial benefits to analyzing and predicting the movements of vehicles and pedestrians around various transportation locations. Such locations are included but not limited to highways, intersections, and roundabouts. By implementing stream processing for predicting vehicle speeds at highways, our application can help improve the accuracy and reliability of traffic speed predictions. This can be a very beneficial tool that can be utilized when enforcing speed limits, alleviating congestion and traffic during peak traffic hours and getting an idea of road patterns based on time and other factors. We aim to utilize various tools and techniques learned throughout the duration of the semester to implement this project.

## Introduction:
In recent years, the increase in traffic and the complexity of road networks have made it difficult to accurately predict the speed of cars on various roads. To overcome this challenge, this project has been developed that leverages various cloud computing tools, distributed systems techniques, and machine learning, to detect road patterns and predict the speed of cars for highways based on different features of cars. This project aims to provide accurate speed prediction for drivers, traffic control centers, and transportation companies. By analyzing various features such as weight and height of the car, this system can generate accurate speed predictions and improve the overall safety and efficiency of the transportation network. This project also uses distributed systems techniques to ensure scalability, reliability, and fault tolerance of the system. 

## Project Objective:
The goal of this project is to design and implement a system that can predict speeds of vehicles on the highway based on the width and height of each vehicle. This project can be used to determine speed limits required on the highway. This project can assist in the development of enabling dynamic speed limits which can be calculated based on the traffic and size of each car. To implement this project, different tools and techniques on Google Cloud Platform (GCP) will be utilized such as Big Query, Dataflow, Google Pub/Sub. These tools were taught in class for project milestones. In addition to these tools, we will be utilizing the highD dataset, which contains the data regarding the velocity, width, and height of vehicles recorded on highways in Germany to train a machine learning model using libraries such as Scikit-Learn. With the utilization of these tools and technologies, we will create an automated pipeline of importing data, processing the data using a machine learning model, and then store and publish our predictions for further analysis.

## System Architecture:

![Archtecture](https://github.com/preetpatel87/Cloud-Computing-Project-Group-T4/blob/main/Final%20Project/images/image16.png)

The above figure describes the architecture of the cloud infrastructure of this project. The project will utilize two BigQuery databases. One of the databases will be used to store test data that needs to be processed to extract data regarding velocity of vehicles based on width and size. This dataset will be populated using CSV data files created from the data collected by sensors (camera).  The other database will be used to store the values of the model prediction which can be utilized for any further analysis. The project will also utilize Google Pub/Sub to publish the model prediction data which can be utilized by any subscriber that requires real-time updated predictions. Dataflow will be used to automate the model predictions. These are the following stages in the Dataflow job:
Read Table: The job begins by reading test data from Bigquery
Filter Data: In this stage, any data that includes missing or invalid data for any of the required features for prediction will be filtered out
Preprocessing Data: Here, the data is prepared for model inference. Any column other than the required data such as the vehicle dimensions will be dropped.
Model Inference: The trained model will perform inference on the processed data to predict the velocity of each vehicle.
a) Pub/Sub publisher: The prediction from the model will be steamed to a pub/sub topic. The data will first get mapped to a json before publishing to the topic. 
b) Write to DB: The prediction will also be permanently stored to a BigQuery table to be used in the future for further analysis.


## Implementation and Results:
In this section, we will discuss the setup, implementation, and results of this project in various steps.


### Before the Job Flow:
Firstly, to set up the project we created a new database in Big Query called Highway_Trajectory. In this database, we will create tables from csv data files containing test data which includes vehicle dimensions data required by the model to predict the velocity of the vehicle on parts of the highway. The following image shows an example of a table containing test data in the dataset:

![Big  Query Dataset with just the test tables.](https://github.com/preetpatel87/Cloud-Computing-Project-Group-T4/blob/main/Final%20Project/images/image15.png)


Next, we uploaded the exported machine learning model to the cloud bucket of this project. This will enable dataflow to download this machine learning model when we import it to the dataflow job to perform model inference. The model was trained using the highD dataset and was exported as a file called ‘velocityPredictor.joblib’ (see appendix for model training screenshots). The following image shows the exported model stored in the cloud bucket: 

![Google Cloud Bucket with the saved model](https://github.com/preetpatel87/Cloud-Computing-Project-Group-T4/blob/main/Final%20Project/images/image3.png)

After storing the exported model, a Pub/Sub topic was created which will be used to stream the output of the model inference. In the Pub/Sub, we created a topic called ‘milestone2_pub’. The following image shows this topic and the subscriber ID that was used in this project:

![Google Pub/Sub Topic](https://github.com/preetpatel87/Cloud-Computing-Project-Group-T4/blob/main/Final%20Project/images/image20.png)

After setting up Big Query, Pub/Sub Topic, and the exported model on the bucket, we had to create the dataflow job. The full script used to create the dataflow job as well as steps to run the application can be found in this github repository link: https://github.com/preetpatel87/Cloud-Computing-Project-Group-T4/blob/main/Final%20Project/prediction.py

Before we continue to execution, we will explain the important parts of this script below:
The image below shows the various stages in the dataflow job. First step in the ReadFromBQ stage where we will read data from the Big Query table. The name and path of the table needs to be provided in the “–input” argument when running the script. Once the data has been read, we will filter the data to remove any data that contains invalid or null values. The “filterRcds” function will check if the data is valid and will return true or false for the job to determine whether the data is valid or invalid. After filtering the data, we will prepare the data for inference in the preprocess data step. In this step we will run the “PreprocessDataDoFn()” function to remove all the required columns from the data. This preprocessing step reflects the processing of the data that was done during the model training. Next, after the data has been processed we will perform the model inference in the Predictions step. In this step, we first download and import the model from the cloud bucket storage. After the model has been imported, we can perform inference on the processed data. We append the velocity predictions along with the data for the next steps where we store and publish the prediction. Lastly, the storage and publishing of the prediction has been split into two parallel branches. In the first branch, we will simply store the data in a Predict table in Big Query using the “WriteToBigQuery” function. For this step, we provide the schema in which the data will be stored, and store the predictions to a table whose name and path has been provided in the output argument. In the second branch, we convert the data from a dictionary to a json and encode it to prepare it before publishing it to the Pub/Sub topic. Lastly, we will publish the prediction data to the topic using the “WriteToPubSub” function. The following images are snapshots of the script and the functions that were discussed above:

Data Flow Steps:
![Data Flow Steps](https://github.com/preetpatel87/Cloud-Computing-Project-Group-T4/blob/main/Final%20Project/images/image5.png)


Filter Data Steps:
![Filter Data Steps](https://github.com/preetpatel87/Cloud-Computing-Project-Group-T4/blob/main/Final%20Project/images/image12.png)


Preprocess Steps:

![Preprocess Steps](https://github.com/preetpatel87/Cloud-Computing-Project-Group-T4/blob/main/Final%20Project/images/image13.png)


Prediction Steps:

![Prediction Steps](https://github.com/preetpatel87/Cloud-Computing-Project-Group-T4/blob/main/Final%20Project/images/image18.png)


## Execution of the Dataflow job:

The image below shows the list of dataflow jobs before running the project dataflow job:

![Dataflow before job run](https://github.com/preetpatel87/Cloud-Computing-Project-Group-T4/blob/main/Final%20Project/images/image2.png)

The image below shows the dataflow job named ‘cloud-proj-demo’ in the running stage. We run the dataflow job using the following command:

python prediction.py    --runner DataflowRunner    --project $PROJECT    --staging_location $BUCKET/staging    --temp_location $BUCKET/temp    --input $PROJECT:Highway_Trajectory.tracks02      --output $PROJECT:Highway_Trajectory.Predict    --region  northamerica-northeast2    --experiment use_unsupported_python_version    --streaming --setup_file ./setup.py --model $BUCKET/project_model --job_name cloud-proj-demo

![Dataflow job in running state](https://github.com/preetpatel87/Cloud-Computing-Project-Group-T4/blob/main/Final%20Project/images/image10.png)

The images below show the dataflow job after it has finished executing predictions on the provided input Big Query table. The first image shows the job status of the job as succeeded and the second image shows all the stages in the dataflow job:

Suceeded Dataflow Job:

![Suceeded Dataflow Job](https://github.com/preetpatel87/Cloud-Computing-Project-Group-T4/blob/main/Final%20Project/images/image11.png)

The stages in the succeeded Dataflow job:

![The stages in the succeeded Dataflow job](https://github.com/preetpatel87/Cloud-Computing-Project-Group-T4/blob/main/Final%20Project/images/image7.png)

## Results:
The following images show the results from the execution of the dataflow job. The first image below shows the Big Query table which was used to store the prediction data. Here we can see the width and height of the vehicle along with the predicted velocity. The second image shows the output of a subscriber script which simply prints the consumed messages.

Big Query prediction output table:

![Big Query prediction output table](https://github.com/preetpatel87/Cloud-Computing-Project-Group-T4/blob/main/Final%20Project/images/image19.png)

Output of  the Pub/Sub subscriber script:

![Output of  the Pub/Sub subscriber script:](https://github.com/preetpatel87/Cloud-Computing-Project-Group-T4/blob/main/Final%20Project/images/image1.png)

## Conclusion:
In conclusion, the team successfully completed the project and met all the project objectives using the knowledge gained from previous project milestones in the Cloud Computing course. The team used tools such as the Big Query, Buckets, Dataflow, and Pub/Sub to implement the cloud infrastructure of the project to streamline making predictions with the trained velocity predictor model. This project demonstrates that the team has gained valuable knowledge and experience with the technologies introduced in class to create cloud infrastructure for any project.

## Appendix
Velocity Predictor Model Training:

![Imports](https://github.com/preetpatel87/Cloud-Computing-Project-Group-T4/blob/main/Final%20Project/images/image6.png)

![Load and Prepare](https://github.com/preetpatel87/Cloud-Computing-Project-Group-T4/blob/main/Final%20Project/images/image8.png)

![Testing Data](https://github.com/preetpatel87/Cloud-Computing-Project-Group-T4/blob/main/Final%20Project/images/image9.png)

![](https://github.com/preetpatel87/Cloud-Computing-Project-Group-T4/blob/main/Final%20Project/images/image17.png)

![](https://github.com/preetpatel87/Cloud-Computing-Project-Group-T4/blob/main/Final%20Project/images/image4.png)

![](https://github.com/preetpatel87/Cloud-Computing-Project-Group-T4/blob/main/Final%20Project/images/image14.png)

