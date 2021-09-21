import json
import sys
import time

from confluent_kafka.cimpl import KafkaError, KafkaException
from confluent_kafka.cimpl import Consumer


def read_from_topic(topic, group_id, max_count):

        conf = {'bootstrap.servers': "localhost:9092",
                'auto.offset.reset': 'smallest',
                'group.id': group_id}

        consumer = Consumer(conf)

        try:
            consumer.subscribe([topic])
            data = []
            msg_count = 0
            last_none = None
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
                    # return render(request, '../templates/django_kafka/django_kafka/telemetry.html',
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
                    print(msg.value())
                    # msg_process(msg)
                    data.append(json.loads(msg.value()))
                    msg_count += 1
                    if msg_count == max_count:
                        return data

                    # if msg_count % MIN_COMMIT_COUNT == 0:
                    consumer.commit()
        finally:
            # Close down consumer to commit final offsets.
            consumer.close()