from django.conf.urls import url

from position import views

urlpatterns = [
    url(r'^update_position/(?P<pk>[0-9]+)/$', views.PositionUpdateView.as_view(), name='update_position'),

    url(r'^add_relation/(?P<pk>[0-9]+)/$', views.AddRelationView.as_view(), name='add_relation'),
    url(r'^relations/$', views.RelationsListView.as_view(), name='relations'),
    url(r'^delete_relation/(?P<pk>[0-9]+)/$', views.DeleteRelationView.as_view(), name='delete_relation'),

    url(r'^delivery_center/(?P<slug>[-\w]+)/$', views.DCDetailView.as_view(), name='delivery_center'),
    url(r'^delivery_centers/$', views.DCListView.as_view(), name='delivery_centers')
]
