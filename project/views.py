from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView
from django.views.generic import DetailView, UpdateView, DeleteView

from dudes9 import settings
from relation.forms import AddProjectForm, CloseProjectForm
from relation.models import Project, Relation


class ProjectsListView(ListView):
    model = Project
    page_title = 'Projects list'
    paginate_by = settings.PAGINATION
    context_object_name = 'projects'
    template_name = 'projects.html'
    queryset = Project.objects.prefetch_related('members', 'technologies').all().order_by('-start_date')

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        if request.GET.get('order_by') and request.GET.get('reverse'):
            self.object_list.query.order_by = ['-' + request.GET['order_by']]
        elif request.GET.get('order_by'):
            self.object_list.query.order_by = [request.GET['order_by']]
        context = self.get_context_data()
        return self.render_to_response(context)


class AddProjectView(CreateView):
    model = Project
    form_class = AddProjectForm
    template_name = 'add_project_form.html'
    success_url = reverse_lazy('projects')


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project_detail.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get('order_by') and request.GET.get('reverse'):
            order = '-' + request.GET['order_by']
        elif request.GET.get('order_by'):
            order = request.GET['order_by']
        else:
            order = 'id'
        self.queryset = Project.objects.prefetch_related(
            Prefetch('relation', Relation.objects.order_by(order),))
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


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
