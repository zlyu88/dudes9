from django.db.models import Prefetch, Case, When
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView
from django.views.generic import DetailView, UpdateView, DeleteView

from dudes9 import settings
from relation.forms import AddProjectForm, CloseProjectForm, AddTechnologyForm
from relation.models import Project, Relation, Technology


class ProjectsListView(ListView):
    model = Project
    page_title = 'Projects list'
    paginate_by = settings.PAGINATION
    context_object_name = 'projects'
    template_name = 'projects.html'
    queryset = Project.objects.prefetch_related('members', 'technologies').all().order_by('-start_date')

    def extra_order(self, request):
        ordering_parameters = {
            'positions': [[project.pk, project.positions().count()] for project in self.object_list],
            'members': [[project.pk, project.active_relations().count()] for project in self.object_list],
            'technologies': [[project.pk, project.technologies.all().count()] for project in self.object_list]
        }

        pk_list = ordering_parameters.get(request.GET.get('order_by'))

        if request.GET.get('reverse'):
            pk_list = [pair[0] for pair in sorted(pk_list, key=lambda tup: tup[1], reverse=True)]
        else:
            pk_list = [pair[0] for pair in sorted(pk_list, key=lambda tup: tup[1])]
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pk_list)])
        queryset = Project.objects.filter(pk__in=pk_list).order_by(preserved)
        return queryset

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        if request.GET.get('order_by') in ['positions', 'members', 'technologies']:
            self.object_list = self.extra_order(request)
        elif request.GET.get('order_by') and request.GET.get('reverse'):
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
        if request.GET.get('order_by') == 'delivery_center':
            order = 'id'
            relations = Relation.objects.filter(project__pk=self.kwargs['pk'])
            pk_list = [[rel.pk, rel.member.delivery_center] for rel in relations]
            if request.GET.get('reverse'):
                pk_list = [pair[0] for pair in sorted(pk_list, key=lambda tup: tup[1], reverse=True)]
            else:
                pk_list = [pair[0] for pair in sorted(pk_list, key=lambda tup: tup[1])]
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pk_list)])
            queryset = Relation.objects.filter(pk__in=pk_list, project__pk=self.kwargs['pk']).order_by(preserved)
        elif request.GET.get('order_by') and request.GET.get('reverse'):
            order = '-' + request.GET['order_by']
        elif request.GET.get('order_by'):
            order = request.GET['order_by']
        else:
            order = 'id'
        self.queryset = Project.objects.prefetch_related(
            Prefetch('relation', Relation.objects.order_by(order),))
        self.object = self.get_object()
        if request.GET.get('order_by') == 'delivery_center':
            self.object._prefetched_objects_cache['relation'] = queryset
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


class AddTechnologyView(CreateView):
    model = Technology
    form_class = AddTechnologyForm
    template_name = 'add_technology_form.html'
    success_url = reverse_lazy('projects')


class TechnologiesListView(ListView):
    model = Technology
    page_title = 'Technologies list'
    paginate_by = settings.PAGINATION
    context_object_name = 'technologies'
    template_name = 'technologies.html'
    ordering = '-title'

    def extra_order(self, request):
        ordering_parameters = {
            'active_projects': [[tech.pk, tech.active_projects().count()] for tech in self.object_list],
            'all_projects': [[tech.pk, tech.projects.all().count()] for tech in self.object_list],
        }

        pk_list = ordering_parameters.get(request.GET.get('order_by'))

        if request.GET.get('reverse'):
            pk_list = [pair[0] for pair in sorted(pk_list, key=lambda tup: tup[1], reverse=True)]
        else:
            pk_list = [pair[0] for pair in sorted(pk_list, key=lambda tup: tup[1])]
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pk_list)])
        queryset = Technology.objects.filter(pk__in=pk_list).order_by(preserved)
        return queryset

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        if request.GET.get('order_by') in ['active_projects', 'all_projects']:
            self.object_list = self.extra_order(request)
        elif request.GET.get('order_by') and request.GET.get('reverse'):
            self.object_list.query.order_by = ['-' + request.GET['order_by']]
        elif request.GET.get('order_by'):
            self.object_list.query.order_by = [request.GET['order_by']]
        context = self.get_context_data()
        return self.render_to_response(context)


class TechnologyDetailView(DetailView):
    model = Technology
    template_name = 'technology_detail.html'

    def extra_order(self, request):
        projects = Project.objects.filter(technologies__pk=self.kwargs['pk'])
        ordering_parameters = {
            'positions': [[project.pk, project.positions().count()] for project in projects],
            'members': [[project.pk, project.active_relations().count()] for project in projects],
            'technologies': [[project.pk, project.technologies.all().count()] for project in projects]
        }

        pk_list = ordering_parameters.get(request.GET.get('order_by'))

        if request.GET.get('reverse'):
            pk_list = [pair[0] for pair in sorted(pk_list, key=lambda tup: tup[1], reverse=True)]
        else:
            pk_list = [pair[0] for pair in sorted(pk_list, key=lambda tup: tup[1])]
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pk_list)])
        queryset = Project.objects.filter(pk__in=pk_list).order_by(preserved)
        return queryset

    def get(self, request, *args, **kwargs):
        if request.GET.get('order_by') in ['positions', 'members', 'technologies']:
            order, extra_order = 'id', self.extra_order(request)
        elif request.GET.get('order_by') and request.GET.get('reverse'):
            order = '-' + request.GET['order_by']
        elif request.GET.get('order_by'):
            order = request.GET['order_by']
        else:
            order = 'id'
        self.queryset = Technology.objects.prefetch_related(
            Prefetch('projects', Project.objects.order_by(order),))
        self.object = self.get_object()
        if request.GET.get('order_by') in ['positions', 'members', 'technologies']:
            self.object._prefetched_objects_cache['projects'] = extra_order
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class TechnologyUpdateView(UpdateView):
    model = Technology
    template_name = 'technology_update.html'
    fields = ['title']

    def get_success_url(self):
        return reverse_lazy('technology_detail', kwargs={'pk': self.kwargs['pk']})
