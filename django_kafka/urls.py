from django.conf.urls import url
from .views import get_data_with_user_name

urlpatterns = [
    url(r'^get_data_with_user_name', get_data_with_user_name, name='get_data_with_user_name'),
]