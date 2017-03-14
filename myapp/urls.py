from django.conf.urls import url
from . import views
from myapp.user.views import CreateUserView
from myapp.test.views import CreateTestView

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/delete/$', views.post_delete, name='post_delete'),
    url(r'^salestracker/regist/$', CreateUserView.as_view()),
    url(r'^salestracker/testapi/$', CreateTestView.as_view()),
]