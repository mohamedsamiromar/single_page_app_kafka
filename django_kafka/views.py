import sys
import time

from confluent_kafka.cimpl import KafkaError, KafkaException
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework import permissions
from .serializer import RegisterSerializer
from rest_framework import generics
from confluent_kafka import Consumer
import json

class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            first_name = serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = User()
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.set_password(password)
            user.save()
            return Response(RegisterSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(RegisterSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(('GET',))
# @renderer_classes((JSONRenderer))
def get_data_with_user_name(request):
    username = request.user.username
    conf = {'bootstrap.servers': "localhost:9092",
            'group.id': username,
            }

    consumer = Consumer(conf)
    topic = request.GET.get('topic')
    max_count = request.GET.get('max_count', 10)  # read from request param or default equal 10

    try:
        consumer.subscribe([topic])
        data = []
        msg_count = 0
        last_none = None
        while True:
            msg = consumer.poll(timeout=3)
            if msg is None:
                if last_none is not None:
                    current = int(time.time() * 1000.0)
                    if current - last_none > 1000:
                        return Response(data, status=status.HTTP_201_CREATED)
                if last_none is None:
                    last_none = int(time.time()*1000.0)
                continue
                # return Response(data, status=status.HTTP_201_CREATED)

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
                    return Response(data, status=status.HTTP_201_CREATED)
                # if msg_count % MIN_COMMIT_COUNT == 0:
                consumer.commit(asynchronous=True)
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()
    return Response(data, status=status.HTTP_201_CREATED)


