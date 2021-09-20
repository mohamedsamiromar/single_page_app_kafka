
from confluent_kafka import Producer
import socket

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

from django_kafka import permission_roles


@user_passes_test(permission_roles.is_login)
def add_data_producer(request):
    conf = {'bootstrap.servers': "localhost:9092",
            'client.id': socket.gethostname()}

    producer = Producer(conf)
    topic = "telemetry"
    producer.produce(topic, key="key", value='{"type":"TELEMETRY", "message_id": "1236a", "payload": [{"a":"b"}]}')
    producer.flush()
    return render(request, '../templates/django_kafka/django_kafka/producer.html',
                  {'message': 'Data sent too kafka successfully'})
