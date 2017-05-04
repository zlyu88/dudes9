from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView
from django.views.generic import DetailView, UpdateView, DeleteView

from dudes9 import settings
from relation.forms import AddMemberForm
from relation.models import Project


class ProjectsListView(ListView):
    model = Project
    page_title = 'Projects list'
    paginate_by = settings.PAGINATION
    context_object_name = 'projects'
    template_name = 'projects.html'
    queryset = Project.objects.prefetch_related('position').all()

