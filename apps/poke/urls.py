from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^register_view$', views.register_view),
    url(r'^login_view$', views.login_view),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
    url(r'^dashboard/(?P<user_id>\d+)$', views.increment),
]
