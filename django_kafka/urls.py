from django.conf.urls import url
from .views import get_data_with_user_name
from .consumer_one import get_data_by_username
urlpatterns = [
    url(r'^get_data_with_user_name', get_data_with_user_name, name='get_data_with_user_name'),
    url(r'^get_data_by_username', get_data_by_username, name='get_data_by_username'),
]