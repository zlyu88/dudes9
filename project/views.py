from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView
from django.views.generic import DetailView, UpdateView, DeleteView

from dudes9 import settings
from relation.forms import AddProjectForm, AddRelationForm, CloseProjectForm
from relation.models import Project, Relation


class ProjectsListView(ListView):
    model = Project
    page_title = 'Projects list'
    paginate_by = settings.PAGINATION
    context_object_name = 'projects'
    template_name = 'projects.html'
    queryset = Project.objects.prefetch_related('members', 'technologies').all()


class AddProjectView(CreateView):
    model = Project
    form_class = AddProjectForm
    template_name = 'add_project_form.html'
    success_url = reverse_lazy('projects')


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project_detail.html'
    queryset = Project.objects.prefetch_related('members', 'relation').all()


class ProjectUpdateView(UpdateView):
    model = Project
    template_name = 'project_update.html'
    fields = ['title', 'technologies']

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.kwargs['pk']})


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'project_delete.html'
    success_url = reverse_lazy('projects')
    queryset = Project.objects.prefetch_related('relation').all()


class CloseProjectView(DeleteView):
    model = Project
    template_name = 'close_project.html'
    form_class = CloseProjectForm
    success_url = reverse_lazy('projects')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.end_date = str(timezone.now())
        self.object.save()

        project = self.object
        relations = Relation.objects.filter(project_id=project.id)
        for relation in relations:
            relation.date_left = project.end_date
            relation.save()
        return HttpResponseRedirect(self.get_success_url())


class AddRelationView(CreateView):
    model = Relation
    form_class = AddRelationForm
    template_name = 'add_relation_form.html'
    success_url = reverse_lazy('projects')


class RelationsListView(ListView):
    model = Relation
    page_title = 'Relations list'
    paginate_by = settings.PAGINATION
    context_object_name = 'relations'
    template_name = 'relations.html'


class DeleteRelationView(DeleteView):
    model = Relation
    template_name = 'delete_relation.html'
    success_url = reverse_lazy('relations')
