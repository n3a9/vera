from django.conf.urls import url
from vera_website import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^input/$', views.AboutPageView.as_view()),
]

