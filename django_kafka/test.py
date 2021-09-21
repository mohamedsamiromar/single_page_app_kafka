import sys

from confluent_kafka.cimpl import KafkaError, KafkaException
from confluent_kafka import Consumer

from django_kafka.kafka_service import read_from_topic

running = True

def basic_consume_loop(consumer, topics):
    try:
        consumer.subscribe(topics)

        while running:
            msg = consumer.poll(timeout=1.0)
            if msg is None: continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                print(msg.value())
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()

def shutdown():
    running = False

read_from_topic('telemetry', 'play1', 100)

# conf = {'bootstrap.servers': "localhost:9092",
#         'group.id': "foo",
#         'auto.offset.reset': 'smallest'}
#
# consumer = Consumer(conf)
# basic_consume_loop(consumer, ['telemetry'])