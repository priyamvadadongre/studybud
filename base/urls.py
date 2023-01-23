from django.urls import path
from . import views
# this urls is for within  app 
urlpatterns=[
    path("",views.home, name="home"),
]