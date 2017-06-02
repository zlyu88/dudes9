from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from dudes9 import settings
from relation.forms import UpdatePositionForm, AddRelationForm
from relation.models import Relation, Member, Project


class PositionUpdateView(UpdateView):
    model = Relation
    template_name = 'position_update.html'
    form_class = UpdatePositionForm
    success_url = reverse_lazy('relations')

    def post(self, request, *args, **kwargs):
        time = str(timezone.now())

        self.object = self.get_object()

        Relation.objects.get(pk=self.object.pk).update(date_left=time)
        # old_relation.update(date_left=time)

        new_relation = Relation(member=self.object.member, position=request.POST['position'],
                                project=self.object.project, date_joined=time)
        new_relation.save()
        return HttpResponseRedirect(self.get_success_url())


class AddRelationView(CreateView):
    model = Relation
    form_class = AddRelationForm
    template_name = 'add_relation_form.html'
    success_url = reverse_lazy('relations')

    def get(self, request, *args, **kwargs):
        self.object = None
        if kwargs.get('pk'):
            self.initial['project'] = Project.objects.filter(pk=kwargs['pk']).first()
        return super(AddRelationView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        time = str(timezone.now())
        self.object = None

        relation = Relation.objects.filter(member_id=request.POST['member'],
                                           project=request.POST['project'],
                                           date_left=None).first()

        if relation and not relation.position == request.POST['position']:
            relation.update(date_left=time)
        return super(AddRelationView, self).post(request, *args, **kwargs)


class RelationsListView(ListView):
    model = Relation
    page_title = 'Relations list'
    paginate_by = settings.PAGINATION
    context_object_name = 'relations'
    template_name = 'relations.html'
    ordering = '-date_joined'

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        if request.GET.get('order_by'):
            self.object_list.query.order_by = ['-' + request.GET['order_by']] if request.GET.get('reverse') \
                else [request.GET['order_by']]
        context = self.get_context_data()
        return self.render_to_response(context)


class DeleteRelationView(DeleteView):
    model = Relation
    template_name = 'delete_relation.html'
    success_url = reverse_lazy('relations')


class DCDetailView(ListView):
    model = Member
    page_title = 'Members list'
    paginate_by = settings.PAGINATION
    context_object_name = 'members'
    template_name = 'DC_detail.html'

    def get(self, request, *args, **kwargs):
        delivery_center = request.resolver_match.kwargs['slug']
        self.object_list = Member.only_members().filter(delivery_center=delivery_center).order_by('-date_joined')
        if request.GET.get('order_by'):
            self.object_list.query.order_by = ['-' + request.GET['order_by']] if request.GET.get('reverse') \
                else [request.GET['order_by']]
        context = self.get_context_data()
        return self.render_to_response(context)


class DCListView(ListView):
    model = Member
    page_title = 'DC list'
    paginate_by = settings.PAGINATION
    context_object_name = 'members'
    template_name = 'DC_list.html'

    def get(self, request, *args, **kwargs):
        self.object_list = Member.locations()
        request.content_params['numbers'] = \
            [(x, Member.only_members().filter(delivery_center=x)) for x in self.object_list]
        context = self.get_context_data()
        return self.render_to_response(context)
