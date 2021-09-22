import sys

from confluent_kafka.admin import ClusterMetadata, TopicMetadata
from confluent_kafka.cimpl import KafkaError, KafkaException, TopicPartition
from confluent_kafka import Consumer

from django_kafka.kafka_service import read_from_topic

running = True

def basic_consume_loop(consumer, topics):
    try:
        consumer.subscribe(topics)
        # current = consumer.position([TopicPartition(topic=topics[0], partition=0)])
        # topicPartition = current[0]
        # print(topicPartition.offset)
        topic_partition = TopicPartition(topics[0], partition=0)
        low, high = consumer.get_watermark_offsets(topic_partition)
        print('%d - %d', low, high)
        # if high > 30:
        #     high -= 30
        topic_partition.offset = high-1
        consumer.assign([topic_partition])
        consumer.seek(topic_partition)

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

# read_from_topic('telemetry', 'play1', 2, True)
#from datetime import datetime
# datetime_str = '2016-10-03T19:00:00.999Z'
# datetime_object = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
# timestamp = datetime_object.timestamp()
# stamp_mills = int(timestamp * 1000)
# print(stamp_mills)
# conf = {'bootstrap.servers': "localhost:9092",
#         'group.id': "foo",
#         'auto.offset.reset': 'smallest'
#         }
#
# consumer = Consumer(conf)
# basic_consume_loop(consumer, ['telemetry'])

a = ''
if a:
    print('hello')