from django.conf.urls import url

from project import views

urlpatterns = [
    url(r'^add_project/$', views.AddProjectView.as_view(), name='add_project'),

    url(r'^projects/$', views.ProjectsListView.as_view(), name='projects'),
    url(r'^project_detail/(?P<pk>[0-9]+)/$', views.ProjectDetailView.as_view(), name='project_detail'),

    url(r'^update_project/(?P<pk>[0-9]+)/$', views.ProjectUpdateView.as_view(), name='update_project'),
    url(r'^delete_project/(?P<pk>[0-9]+)/$', views.ProjectDeleteView.as_view(), name='delete_project'),

    url(r'^close_project/(?P<pk>[0-9]+)/$', views.CloseProjectView.as_view(), name='close_project'),


    url(r'^add_technology/$', views.AddTechnologyView.as_view(), name='add_technology'),

    url(r'^technologies/$', views.TechnologiesListView.as_view(), name='technologies'),
    url(r'^technology_detail/(?P<pk>[0-9]+)/$', views.TechnologyDetailView.as_view(), name='technology_detail'),
    url(r'^update_technology/(?P<pk>[0-9]+)/$', views.TechnologyUpdateView.as_view(), name='update_technology'),
]
