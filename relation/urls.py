from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout
from django.contrib.auth.views import password_reset, password_reset_done
from django.contrib.auth.views import password_reset_confirm, password_reset_complete
from django.urls import reverse_lazy

from dudes9 import settings
from relation import views
from relation.forms import EmailLoginForm

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^add_member/$', views.AddMemberView.as_view(), name='add_member'),
    url(r'^login/$', login, name="login", kwargs={"authentication_form": EmailLoginForm,
                                                  'template_name': 'login.html'}),
    url(r'^logout/', logout, {'next_page': reverse_lazy('index')}, name='logout'),

    url(r'^members/$', views.MembersListView.as_view(), name='members'),
    url(r'^member/(?P<pk>[0-9]+)/$', views.MemberView.as_view(), name='member'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.MemberUpdate.as_view(), name='update'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.MemberDelete.as_view(), name='delete'),

    url(r'^member_projects/(?P<pk>[0-9]+)/$', views.MemberProjectsView.as_view(), name='member_projects'),
    # url(r'^member_history/(?P<pk>[0-9]+)/$', views.MemberHistoryView.as_view(), name='member_history'),

    url(r'^leave_project/(?P<pk>[0-9]+)/$', views.MemberLeftProject.as_view(), name='leave_project'),

    url(r'^change_password/(?P<pk>[0-9]+)/$', views.ChangePasswordView.as_view(), name='change_password'),

    url(r'^password/reset/$', password_reset, name='password_reset',
        kwargs={'template_name': 'password_reset_form.html'}),
    url(r'^password/reset/done/$', password_reset_done, name='password_reset_done',
        kwargs={'template_name': 'password_reset_done.html'}),
    url(r'^password/reset/complete/$', password_reset_complete, name='password_reset_complete',
        kwargs={'template_name': 'password_reset_complete.html'}),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm, name='password_reset_confirm',
        kwargs={'template_name': 'password_reset_confirm.html'}),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
