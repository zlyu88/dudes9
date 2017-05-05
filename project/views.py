from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic import DetailView, UpdateView, DeleteView

from dudes9 import settings
from relation.forms import AddProjectForm, AddRelationForm
from relation.models import Project, Relation


class ProjectsListView(ListView):
    model = Project
    page_title = 'Projects list'
    paginate_by = settings.PAGINATION
    context_object_name = 'projects'
    template_name = 'projects.html'


class AddProjectView(CreateView):
    model = Project
    form_class = AddProjectForm
    template_name = 'add_project_form.html'
    success_url = reverse_lazy('projects')


class AddRelationView(CreateView):
    model = Relation
    form_class = AddRelationForm
    template_name = 'add_relation_form.html'
    success_url = reverse_lazy('projects')


# class MembersListView(ListView):
#     model = Member
#     page_title = 'Members list'
#     paginate_by = settings.PAGINATION
#     context_object_name = 'members'
#     template_name = 'members.html'
#     queryset = Member.objects.select_related('delivery_center').all()
#
#
# class ProfileView(DetailView):
#     model = Member
#     template_name = 'profile.html'
#     queryset = Member.objects.select_related('delivery_center').all()
#
#
# class MemberUpdate(UpdateView):
#     model = Member
#     template_name = 'member_update.html'
#     fields = ['username']
#     success_url = reverse_lazy('members')
#
#
# class MemberDelete(DeleteView):
#     model = Member
#     template_name = 'member_delete.html'
#     success_url = reverse_lazy('members')
#
#
# class MemberProjectsView(DetailView):
#     model = Member
#     template_name = 'member_projects.html'
#     queryset = Member.objects.prefetch_related('relation').all()

