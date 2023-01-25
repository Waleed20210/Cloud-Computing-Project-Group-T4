# Milestone 1: Data Ingestion System (Apache Kafka)

## Objective:
1. Understand the role of Data Ingestion System in Event Driven Architecture.
2. Get familiar with Kafka and its terminologies.
3. Be able to create topics, producers, and consumers via GUI and code.
4. Get familiar with Google Pub/sub.

## Repository:
https://github.com/GeorgeDaoud3/SOFE4630U-MS1

### Discussion
- What is EDA?
    > EDA (Event Driven Architecture) is a software architecture that relies on a system or application reacting to a specific action made by an external entity
- Advantages
    > - Allows for high cohesion and low coupling
    > - Allows for use of other types of architecture such as microservices
    > - Scallable
- [Disadvantages](https://www.techtarget.com/searchapparchitecture/tip/Event-driven-architecture-pros-and-cons-Is-EDA-worth-it)
    > - Duplicated Events
    > - Error handling
    > - Naming
- In Kafka, what’s meant by cluster, broker, topic, replica, partition, zookeeper, controller, leader, consumer, producer, and consumer group?
    > - __cluster__: a system with brokers, topics, partitions, zookeeper etc.
    > - __broker__: a distributed system that manages the events in motion and stores them oh physical hard drives
    > - __topic__: An item in a registry that is associated with a specific stream of data
    > - __replica__: a copy of the data or element across multiple servers
    > - __partition__: a distribution of data across multiple servers and hard drives on a broker for parallel work loads(e.g. reading and writing data)
    > - __zookeeper__: A meta data storage for a kafka cluster that allows for managing producers, consumers and leader election of brokers
    > - __controller__: controlls the election of leaader brokers
    > - __leader__: a leader broker at which operations access first
    > - __consumer__: subscribes to data published by producers
    > - __producer__: publishes data to the cluster for subscription by the consumer(groups)
    > - __consumer group__: a collective group of consumers who are interested in the same topic