from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/delete/$', views.post_delete, name='post_delete'),
    url(r'^salestracker/regist/$', views.user_regist, name='user_regist'),
    url(r'^salestracker/testapi/$', views.user_regist, name='user_regist'),
	url(r'^salestracker/checkphone/$', views.checkphone, name='checkphone'),
	url(r'^salestracker/getuserlocation/$', views.getuserlocation, name='getuserlocation'),
	url(r'^salestracker/saveuserlocation/$', views.saveuserlocation, name='saveuserlocation'),
	url(r'^salestracker/getallusers/$', views.getallusers, name='getallusers'),
	url(r'^salestracker/getalllocations/$', views.getalllocations, name='getalllocations'),
	url(r'^salestracker/removeuserbyphonenumber/$', views.removeuserbyphonenumber, name='removeuserbyphonenumber'),
	url(r'^salestracker/removeuserlocationbyphonenumber/$', views.removeuserlocationbyphonenumber, name='removeuserlocationbyphonenumber'),
	url(r'^salestracker/getalllocationsforcurrentday/$', views.getalllocationsforcurrentday, name='getalllocationsforcurrentday'),
]
