from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from .kafka_service import read_from_topic
from django_kafka import permission_roles
from .utils import str_to_timestamp


@user_passes_test(permission_roles.is_login)
def get_feedback_from_last_offset(request):
    if request.method == "GET":
        username = request.user.username
        topic = "feedback"
        data = read_from_topic(topic, username)
        return render(request, '../templates/django_kafka/feedback/feedback-last-offest.html',
                      {'topic_data': data})


@user_passes_test(permission_roles.is_login)
def get_feedback_from_last_n_Message(request):
    if request.method == "GET":
        username = request.user.username
        topic = "feedback"
        last_n_message = request.GET.get('last_n_message', 30)  # read from request param or default equal 10
        data = read_from_topic(topic, username, int(last_n_message), False)
        return render(request, '../templates/django_kafka/feedback/feedback-last-massage.html',
                      {'topic_data': data})


@user_passes_test(permission_roles.is_login)
def get_feedback_from_beginning(request):
    if request.method == "GET":
        username = request.user.username
        topic = "telemetry"
        data = read_from_topic(topic, username, None, True)
        return render(request, '../templates/django_kafka/feedback/feedback-from-beginng.html',
                      {'topic_data': data})


@user_passes_test(permission_roles.is_login)
def get_feedback_between_timestamps(request):
    if request.method == "GET":
        username = request.user.username
        topic = "feedback"
        from_timestamp = None
        from_date_str = request.GET.get('from_date')  # read from request param or default equal 10
        if from_date_str:
            from_timestamp = str_to_timestamp(from_date_str)
        to_timestamp = None
        to_date_str = request.GET.get('to_date')  # read from request param or default equal 10
        if to_date_str:
            to_timestamp = str_to_timestamp(to_date_str)

        if from_timestamp is None and to_timestamp is None:
            return render(request, '../templates/django_kafka/feedback/feedback-timestamps.html',
                          {'topic_data': []})

        data = read_from_topic(topic, username, None, True, from_timestamp, to_timestamp)
        return render(request, '../templates/django_kafka/feedback.html',
                      {'topic_data': data})
