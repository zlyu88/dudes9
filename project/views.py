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


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project_detail.html'
    queryset = Project.objects.prefetch_related('members', 'relation').all()


class ProjectUpdateView(UpdateView):
    model = Project
    template_name = 'project_update.html'
    fields = ['title', 'technologies']
    success_url = reverse_lazy('projects')


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'project_delete.html'
    success_url = reverse_lazy('projects')
    queryset = Project.objects.prefetch_related('relation').all()
