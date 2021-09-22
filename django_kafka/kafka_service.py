import json
import sys
import time
from confluent_kafka.cimpl import KafkaError, KafkaException, TopicPartition
from confluent_kafka.cimpl import Consumer
from confluent_kafka import OFFSET_BEGINNING


def read_from_topic(topic, group_id, last_n_messages=None, from_beginning=False, from_timestamp=None, to_timestamp=None):

        conf = {'bootstrap.servers': "localhost:9092",
                'auto.offset.reset': 'smallest',
                'group.id': group_id}

        consumer = Consumer(conf)
        topic_partition = TopicPartition(topic, partition=0)
        low, high = consumer.get_watermark_offsets(topic_partition)
        if last_n_messages :
            if high > last_n_messages:
                high -= last_n_messages
            topic_partition.offset = high
            consumer.assign([topic_partition])
            consumer.seek(topic_partition)
        elif from_beginning:
            topic_partition = TopicPartition(topic, partition=0)
            topic_partition.offset = OFFSET_BEGINNING
            consumer.assign([topic_partition])
            consumer.seek(topic_partition)

        try:
            consumer.subscribe([topic])
            data = []
            last_none = None
            i: int = 0
            while True:
                msg = consumer.poll(timeout=2)
                if msg is None:
                    if last_none is not None:
                        current = int(time.time() * 1000.0)
                        if current - last_none > 1000:
                            return data
                    if last_none is None:
                        last_none = int(time.time() * 1000.0)
                    continue
                    # return render(request, '../templates/django_kafka/django_kafka/telemetry-home.html',
                    #               {'topic_data': data})

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                         (msg.topic(), msg.partition(), msg.offset()))
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    last_none = None
                    print(type(msg.timestamp()))
                    print(msg.timestamp())
                    print(i, msg.value())

                    valid_message = True
                    if from_timestamp:
                        if msg.timestamp() < from_timestamp:
                            return data
                    if to_timestamp:
                        if msg.timestamp() > to_timestamp:
                            valid_message = False
                    if valid_message:
                        data.append(json.loads(msg.value()))

                    consumer.commit()
                    i += 1
        finally:
            # Close down consumer to commit final offsets.
            consumer.close()