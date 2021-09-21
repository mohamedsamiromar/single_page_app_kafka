from django.conf.urls import url
from .telemetry import get_topic_telemetry
from .producer import add_data_producer
from .commands import get_topic_commands
from .feedback import get_topic_feedback

urlpatterns = [
    url(r'^telemetry', get_topic_telemetry, name='telemetry'),
    url(r'^commands', get_topic_commands, name='commands'),
    url(r'^feedback', get_topic_feedback, name='feedback'),
    url(r'^add_data_producer', add_data_producer, name='add_data_producer'),
]

