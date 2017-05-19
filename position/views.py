from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from dudes9 import settings
from relation.forms import UpdatePositionForm, AddRelationForm
from relation.models import Relation


class PositionUpdateView(UpdateView):
    model = Relation
    template_name = 'position_update.html'
    form_class = UpdatePositionForm
    success_url = reverse_lazy('relations')

    def post(self, request, *args, **kwargs):
        time = str(timezone.now())

        self.object = self.get_object()

        old_relation = Relation.objects.get(pk=self.object.pk)
        old_relation.date_left = time
        old_relation.save()

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
        return super(AddRelationView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        time = str(timezone.now())
        self.object = None

        try:
            relation = Relation.objects.get(member_id=request.POST['member'], project=request.POST['project'],
                                            date_left=None)
        except ObjectDoesNotExist:
            relation = None

        if relation and not relation.position == request.POST['position']:
            relation.date_left = time
            relation.save()

            return super(AddRelationView, self).post(request, *args, **kwargs)
        else:
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
        if request.GET.get('order_by') and request.GET.get('reverse'):
            self.object_list.query.order_by = ['-' + request.GET['order_by']]
        elif request.GET.get('order_by'):
            self.object_list.query.order_by = [request.GET['order_by']]
        context = self.get_context_data()
        return self.render_to_response(context)


class DeleteRelationView(DeleteView):
    model = Relation
    template_name = 'delete_relation.html'
    success_url = reverse_lazy('relations')
