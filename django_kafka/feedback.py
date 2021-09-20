import sys
import time
from confluent_kafka.cimpl import KafkaError, KafkaException
from confluent_kafka import Consumer
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django_kafka import permission_roles


@user_passes_test(permission_roles.is_login)
def get_topic_feedback(request):
    if request.method == "GET":
        username = request.user.username
        conf = {'bootstrap.servers': "localhost:9092",
                'group.id': username}

        consumer = Consumer(conf)
        topic = "feedback"
        max_count = request.GET.get('max_count', 10)  # read from request param or default equal 10

        try:
            consumer.subscribe([topic])
            data = []
            msg_count = 0
            last_none = None
            while True:
                msg = consumer.poll(timeout=1.5)
                if msg is None:
                    if last_none is not None:
                        current = int(time.time() * 1000.0)
                        if current - last_none > 1000:
                            return render(request, '../templates/django_kafka/feedback.html',
                                          {'topic_data': data})
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
                    # data.append(json.loads(msg.value()))
                    msg_count += 1
                    if msg_count == max_count:
                        return render(request, '../templates/django_kafka/feedback.html',
                                      {'topic_data': data})
                    # if msg_count % MIN_COMMIT_COUNT == 0:
                    consumer.commit(asynchronous=True)
        finally:
            # Close down consumer to commit final offsets.
            consumer.close()
        return render(request, '../templates/django_kafka/feedback.html',
                      {'topic_data': data})
