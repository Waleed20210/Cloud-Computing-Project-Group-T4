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

![Archtecture]([Final Project/images/image16.png](https://github.com/preetpatel87/Cloud-Computing-Project-Group-T4/blob/main/Final%20Project/images/image16.png))
