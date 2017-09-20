from django.conf.urls import url
from . import views           # This line is new!

urlpatterns = [
    url(r'^$', views.index),     # This line has changed!
    url(r'^add_user$', views.add_user), 
    url(r'^success$', views.success), 
     url(r'^login$', views.login), 
]