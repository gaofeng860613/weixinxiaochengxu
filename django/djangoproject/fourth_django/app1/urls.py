from django.urls import path,include
# import app1.views
from app1.views import *


urlpatterns = [
    path('hello/', index)
]
