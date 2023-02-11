from django.conf.urls import url

from core import views

app_name = 'core'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.add, name='add'),
    url(r'^done/$', views.done, name='done'),

]
