# Milestone 2: Data Storage and Kafka connects


## Objective:
* Get familiar with Docker images and containers.
* Deploy Tabular and key-Value data storage using GKE.
* Get familiar with Key-Value data storage.
* Get familiar with Kafka Connects and their configuration.

## Repository:
[https://github.com/GeorgeDaoud3/SOFE4630U-MS3](https://github.com/GeorgeDaoud3/SOFE4630U-MS3)

## Discussion:
* How do Kafka connectors maintain availability? [Reference](https://docs.confluent.io/platform/current/connect/design.html#architecture)
    > Kafka connectors are worker processes that work alongside Kafka. These processes are containers that execute tasks defined in the connector instances. Tasks are distributed among available workers.
* MySQL connector supports three serialize/deserialize methods; JSON, AVRO, and PROTOBUF. What are the advantages and disadvantages of each.
    > Nothing. Each schema has different syntax and means of encoding/decoding your message. If compared on the basis of message size, avro is better as its a fit for BigData uses, while protobuf is better for encoding. If data structure isn't large, json is adequate.
* There are two options for **Insert mode** (**UPSERT** or **INSERT**) can be configured for MySQL sink connector. Compare both of them and provide a test case for each of them. [Reference1](https://dev.mysql.com/worklog/task/?id=9807#:~:text=The%20UPSERT%20command%20is%20a,should%20be%20used%20for%20implementation.), [Reference2](https://docs.astera.com/projects/faqs/en/latest/transformations/actions-for-data-loading.html#:~:text=The%20INSERT%20option%20pushes%20the,that%20are%20inserted%20or%20updated.)
    > **Upsert:** is a mix of performing inser/update. This operation depends on if the record is available in the database.
    > **Insert:** simply adds the entry as a new record regardless of if it existed before.
* Confluent Cloud Kafka supports connectors while Google Pub/Sub doesn't support them. What are the advantages and disadvantages of adding connectors to any pub/sub service?
    > Asynchronous operations between Kafka and the source/sink connector. Smaller service ecosystem. I.e. no need to deploy a full service dedicated to writing/parsing/decoding events to MySQL and inviting a point of failure. The connector handles the pushing to/from the source/sink applicaitons.

    > Disadvantages: tight coupling
### Design
- Python source code attached.
- [https://drive.google.com/file/d/1-nedDo0bMYRM-Oq_YVPeEnY5oM8yig2Z/view?usp=share_link](https://drive.google.com/file/d/1-nedDo0bMYRM-Oq_YVPeEnY5oM8yig2Z/view?usp=share_link).