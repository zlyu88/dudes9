from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView, TemplateView
from django.views.generic import DetailView, UpdateView, DeleteView

from dudes9 import settings
from relation.forms import AddMemberForm, LeaveProjectForm
from relation.models import Member, Relation


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
    queryset = Member.only_members().order_by('-date_joined')

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        if request.GET.get('order_by'):
            self.object_list.query.order_by = ['-' + request.GET['order_by']] if request.GET.get('reverse') \
                else [request.GET['order_by']]

        context = self.get_context_data()
        return self.render_to_response(context)


class MemberView(DetailView):
    model = Member
    template_name = 'member.html'


class MemberUpdate(UpdateView):
    model = Member
    template_name = 'member_update.html'
    fields = ['username', 'image']

    def get_success_url(self):
        return reverse_lazy('member', kwargs={'pk': self.kwargs['pk']})


class MemberDelete(DeleteView):
    model = Member
    template_name = 'member_delete.html'
    success_url = reverse_lazy('members')


class MemberProjectsView(DetailView):
    model = Member
    template_name = 'member_projects.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get('order_by') and request.GET.get('reverse'):
            order = '-' + request.GET['order_by']
        elif request.GET.get('order_by'):
            order = request.GET['order_by']
        else:
            order = 'id'
        self.queryset = Member.objects.prefetch_related(
            Prefetch('relation', Relation.objects.order_by(order),))
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class MemberLeftProject(DeleteView):
    model = Relation
    template_name = 'member_left_project.html'
    form_class = LeaveProjectForm
    success_url = reverse_lazy('members')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.date_left = str(timezone.now())
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

#
# class MemberHistoryView(DetailView):
#     model = Member
#     template_name = 'member_history.html'
#     queryset = Member.objects.prefetch_related('relation').all()
