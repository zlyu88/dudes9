from django.conf.urls import url
from django.contrib.auth.views import login, logout
from django.urls import reverse_lazy

from relation import views
from relation.forms import EmailLoginForm

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^add_member/$', views.AddMemberView.as_view(), name='add_member'),
    url(r'^login/$', login, name="login", kwargs={"authentication_form": EmailLoginForm,
                                                  'template_name': 'login.html'}),
    url(r'^logout/', logout, {'next_page': reverse_lazy('index')}, name='logout'),

    url(r'^members/$', views.MembersListView.as_view(), name='members'),
    url(r'^profile/(?P<pk>[0-9]+)/$', views.ProfileView.as_view(), name='profile'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.MemberUpdate.as_view(), name='update'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.MemberDelete.as_view(), name='delete'),

    # url(r'^member_positions/(?P<pk>[0-9]+)/$', views.MemberPositionsView.as_view(), name='member_positions'),
    url(r'^member_projects/(?P<pk>[0-9]+)/$', views.MemberProjectsView.as_view(), name='member_projects'),
    # url(r'^member_history/(?P<pk>[0-9]+)/$', views.MemberHistoryView.as_view(), name='member_history'),

    url(r'^leave_project/(?P<pk>[0-9]+)/$', views.MemberLeftProject.as_view(), name='leave_project'),
]
