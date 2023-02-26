from django.conf.urls import url

from core import views

app_name = 'core'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^done/$', views.done, name='done'),
    url(r'^info/(?P<uuid_string>[\w\-]+).gif$', views.info, name='info'),
    url(r'^journals/$', views.info_table, name='info_table'),
    url(r'^journals/(?P<info_id>\d+)/$', views.journal_table,
        name='journal_table'),
    url(r'^mailings/$', views.mailing_table, name='mailing_table'),
    url(r'^mailings/create/$', views.MailingCreateView.as_view(),
        name='mailing_create'),
    url(r'^mailings/(?P<pk>\d+)/$', views.MailingDetailView.as_view(),
        name='mailing_detail'),
    url(r'^mailings/(?P<pk>\d+)/delete/$', views.MailingDeleteView.as_view(),
        name='mailing_delete'),
    url(r'^mailings/(?P<pk>\d+)/edit/$', views.MailingUpdateView.as_view(),
        name='mailing_edit'),
    url(r'^mailings/(?P<mailing_id>\d+)/send/$', views.mailing_send_form,
        name='mailing_send_form'),
    url(r'^mailings/(?P<mailing_id>\d+)/subscribe/$', views.mailing_subscribe,
        name='mailing_subscribe'),
    url(r'^mailings/(?P<mailing_id>\d+)/subscribe/(?P<user_id>\d+)/$',
        views.mailing_subscribe_user,
        name='mailing_subscribe_user'),
    url(r'^mailings/(?P<mailing_id>\d+)/unsubscribe/(?P<user_id>\d+)/$',
        views.mailing_unsubscribe_user,
        name='mailing_unsubscribe_user'),
    url(r'^mailings/(?P<mailing_id>\d+)/users/$', views.mailing_users,
        name='mailing_users'),
    url(r'^users/$', views.user_table, name='user_table'),
    url(r'^users/create/$', views.UserCreateView.as_view(),
        name='user_create'),
    url(r'^users/(?P<pk>\d+)/$', views.UserDetailView.as_view(),
        name='user_detail'),
    url(r'^users/(?P<pk>\d+)/delete/$', views.UserDeleteView.as_view(),
        name='user_delete'),
    url(r'^users/(?P<pk>\d+)/edit/$', views.UserUpdateView.as_view(),
        name='user_edit'),
]
