from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView
from django.views.generic import DetailView, UpdateView, DeleteView

from dudes9 import settings
from relation.forms import AddMemberForm
from relation.models import Member


class IndexView(TemplateView):
    page_title = 'Index'
    template_name = 'index.html'


class AddMemberView(CreateView):
    model = Member
    form_class = AddMemberForm
    template_name = 'add_member_form.html'
    success_url = reverse_lazy('index')


class MembersListView(ListView):
    model = Member
    page_title = 'Members list'
    paginate_by = settings.PAGINATION
    context_object_name = 'members'
    template_name = 'members.html'
    queryset = Member.objects.select_related('delivery_center').all()


class ProfileView(DetailView):
    model = Member
    template_name = 'profile.html'
    queryset = Member.objects.select_related('delivery_center').all()


class MemberUpdate(UpdateView):
    model = Member
    template_name = 'member_update.html'
    fields = ['username']
    success_url = reverse_lazy('members')


class MemberDelete(DeleteView):
    model = Member
    template_name = 'member_delete.html'
    success_url = reverse_lazy('members')


class MemberProjectsView(DetailView):
    model = Member
    template_name = 'member_projects.html'
    queryset = Member.objects.prefetch_related('relation').all()
