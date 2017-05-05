from django.conf.urls import url

from project import views

urlpatterns = [
    url(r'^add_relation/$', views.AddRelationView.as_view(), name='add_relation'),
    url(r'^add_project/$', views.AddProjectView.as_view(), name='add_project'),
    url(r'^projects/$', views.ProjectsListView.as_view(), name='projects'),
    # url(r'^profile/(?P<pk>[0-9]+)/$', views.ProfileView.as_view(), name='profile'),
    # url(r'^update/(?P<pk>[0-9]+)/$', views.MemberUpdate.as_view(), name='update'),
    # url(r'^delete/(?P<pk>[0-9]+)/$', views.MemberDelete.as_view(), name='delete'),
]
