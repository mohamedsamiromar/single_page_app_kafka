# Kafka Django UI

This project is meant to serve up a single page Django app that allows a user to read data from a particular kafka cluster. This application should only allow users to read data from Kafka, not write any data.

## Setup

In this project, you will find a docker-compose.yml that helps you start up a kafka container locally. To get it running, please run `docker compose up -d` from within this directory.

Additionally, after the kafka container is up and running, please use the `populate_kafka_data.sh` script to push data to the kafka container. This script will push sample data to all topics that are meant to be accessible by this UI (see the Deliverables section for more details). If you'd like to manually read all messages on a particular topic after you have started the relevant docker containers using docker compose, you can use the following command (replacing `MY_TOPIC` with whichever topic you want to query): `docker exec -it kafka-django-ui_kafka_1 /bin/bash -c "kafka-console-consumer --bootstrap-server localhost:9092 --topic MY_TOPIC --from-beginning"`

Lastly, please make sure to run the application you build through a python 3 container - feel free to edit the docker compose yml to enable you to run it alongside the kafka container. Please also use the included requirements.txt file to make sure your application uses the same versions of Django and other libraries that the rest of our platform currently uses.

## Deliverables

The core deliverable of this project is to provide a single page app, built using Django, that allows a user to read data from a specific set of topics.

The set of topics that should be accessible are the following (and only the following):
* `telemetry`
* `commands`
* `feedback`
Please make sure the user is not able to access any other topics apart from these. The set of allowed topics should be easy to adjust in the future as necessary (assuming either a configuration or code change).

When reading data, the data should display in a tabular format in the UI, allowing the user to see the timestamp of each message and inspect the contents of each message. Please note that all messages going on these topics is JSON, so the UI should render it accordingly (it should be relatively easy to read). Additionally, the UI should only try to read data from kafka when the user prompts it to (say, with a click of a button) - it does not need to be continuously reading from kafka, as that is not the use case here. This application should also make sure that the consumer group ids that get used when it queries for data from kafka are short-lived, so that any monitoring checks do not find any consumer groups from the UI that have a large kafka lag.

Lastly, when attempting to read the data from kafka, the UI should ask the user for some filtering inputs:
* the user *must* select one of the following options to query kafka, to ensure efficient performance:
    1. Query from latest offset, and provide the number of messages to read per partition from the latest offset backwards.
    2. Query from the earliest offset, and provide the number of messages to read per partition from the earliest offset forwards.
    3. Query for all messages that were posted between 2 UTC timestamps
* In addition to the above, there should be an optional string search capability that filters the results to only those where the message contains a string that matches the input provided


