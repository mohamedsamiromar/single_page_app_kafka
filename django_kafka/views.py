from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from .serializer import RegisterSerializer
# from kafka import KafkaConsumer


class Register(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = User()
            user.username = serializer.username
            user.set_password(serializer.password)
            user.first_name = serializer.first_name
            user.last_name = serializer.last_name
            user.email = serializer.email
            user.save()
            serializer.save()
            return Response(RegisterSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(RegisterSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(('GET',))
#@renderer_classes((JSONRenderer))
def get_data_with_user_name(request):
    print('here 1')
    # consumer = KafkaConsumer('telemetry', group_id=request.GET['username'])
    msgs = []
    # print('here 2')
    # msg = consumer.get_messages(timeout=1)
    # while msg:
    #     print('itr')
    #     msgs.append(msg)
    return Response(msgs, status=status.HTTP_201_CREATED)



