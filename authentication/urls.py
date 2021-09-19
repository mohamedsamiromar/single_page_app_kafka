from django.conf.urls import url
from authentication import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^signup/', views.signup, name='signup')

]
