from django.conf.urls import url

from project import views

urlpatterns = [
    # url(r'^add_member/$', views.AddMemberView.as_view(), name='add_member'),
    url(r'^projects/$', views.ProjectsListView.as_view(), name='projects'),
    # url(r'^profile/(?P<pk>[0-9]+)/$', views.ProfileView.as_view(), name='profile'),
    # url(r'^update/(?P<pk>[0-9]+)/$', views.MemberUpdate.as_view(), name='update'),
    # url(r'^delete/(?P<pk>[0-9]+)/$', views.MemberDelete.as_view(), name='delete'),
]
