from django.conf.urls import url
from django.views.generic import TemplateView

from .telemetry import get_telemetry_from_last_offset, get_telemetry_from_last_n_Message, get_telemetry_from_beginning, get_telemetry_between_timestamps
from .producer import add_data_producer
from .commands import get_commands_from_last_offset, get_commands_from_last_n_Message, get_commands_from_beginning, get_commands_between_timestamps, commands_home
from .feedback import get_feedback_from_last_n_Message, get_feedback_from_last_offset, get_feedback_from_beginning, get_feedback_between_timestamps

urlpatterns = [
    # Telemetry
    # url('telemetry-home', TemplateView.as_view(template_name='../templates/django_kafka/telemetry/telemetry-home.html'),
    #     name="telemetry-home"),
    url(r'^telemetry-last-offest', get_telemetry_from_last_offset, name='telemetry-last-offest'),
    url(r'^telemetry-last-massage', get_telemetry_from_last_n_Message, name='telemetry-last-massage'),
    url(r'^telemetry-from-beginng', get_telemetry_from_beginning, name='telemetry-from-beginng'),
    url(r'^telemetry-timestamps', get_telemetry_between_timestamps, name='telemetry-timestamps'),


    # commands
    # url('commands-home', TemplateView.as_view(template_name='../templates/django_kafka/commands/commands-home.html'),
    #     name="commands-home"),

    # url(r'^commands-home', commands_home, name='commands-home'),
    url(r'^commands-last-offest', get_commands_from_last_offset , name='commands-last-offest'),
    url(r'^commands-last-massage', get_commands_from_last_n_Message, name='commands-last-massage'),
    url(r'^commands-from-beginng', get_commands_from_beginning, name='commands-from-beginng'),
    url(r'^commands-timestamps', get_commands_between_timestamps, name='commands-timestamps'),

    # feedback
    # url('feedback-home', TemplateView.as_view(template_name='../templates/django_kafka/feedback/feedback-home.html'),
    #     name="feedback-home"),
    url(r'^feedback-last-offest', get_feedback_from_last_offset, name='feedback-last-offest'),
    url(r'^feedback-last-massage', get_feedback_from_last_n_Message, name='feedback-last-massage'),
    url(r'^feedback-from-beginng', get_feedback_from_beginning, name='feedback-from-beginng'),
    url(r'^feedback-timestamps', get_feedback_between_timestamps, name='feedback-timestamps'),


    url(r'^add_data_producer', add_data_producer, name='add_data_producer'),
]