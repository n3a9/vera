from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()
import apps.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', apps.views.index, name='index'),
    url(r'^input/', apps.views.input, name='input'),
]
