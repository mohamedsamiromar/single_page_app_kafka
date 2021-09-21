from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from .kafka_service import read_from_topic
from django_kafka import permission_roles


@user_passes_test(permission_roles.is_login)
def get_topic_telemetry(request):
    if request.method == "GET":
        username = request.user.username
        topic = "telemetry"
        max_count = request.GET.get('max_count', 10)  # read from request param or default equal 10
        data = read_from_topic(topic, username, int(max_count))
        return render(request, '../templates/django_kafka/telemetry.html',
                      {'topic_data': data})
