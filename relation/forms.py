from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelChoiceField, ModelMultipleChoiceField
from django.utils import timezone

from relation.models import Member, Technology, Project, Relation


class EmailLoginForm(AuthenticationForm):
    username = UsernameField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': ''}),
        label='Email')

    error_messages = {
        'invalid_login': (
            "Please enter a correct email and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': ("This account is inactive."),
    }

    def clean(self):
        try:
            self.cleaned_data["username"] = get_user_model().objects.get(email=self.data["username"])
        except ObjectDoesNotExist:
            self.cleaned_data["username"] = "a_username_that_do_not_exists_anywhere_in_the_site"
        return super(EmailLoginForm, self).clean()


class AddMemberForm(UserCreationForm):
    username = forms.CharField(max_length=255, help_text='Required. Inform a valid username.')
    email = forms.EmailField(max_length=50, help_text='Required. Inform a valid email address.')
    image = forms.ImageField(required=False, label='Select a file')

    class Meta:
        model = Member
        fields = ('delivery_center', 'username', 'email', 'password1', 'password2', 'image')


class AddProjectForm(forms.ModelForm):
    title = forms.CharField(max_length=255)
    technologies = ModelMultipleChoiceField(queryset=Technology.objects.all())

    class Meta:
        model = Relation
        fields = ('title', 'technologies')

    def save(self):
        data = self.cleaned_data
        project = Project(title=data['title'], start_date=str(timezone.now()))
        project.save()
        for tech in data['technologies']:
            project.technologies.add(tech)
        project.save()
        return project


class AddRelationForm(forms.ModelForm):
    member = ModelChoiceField(queryset=Member.objects.all())
    project = ModelChoiceField(queryset=Project.objects.all())

    class Meta:
        model = Relation
        fields = ('member', 'position', 'project')


class CloseProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('end_date',)
        widgets = {'end_date': forms.HiddenInput()}


class LeaveProjectForm(forms.ModelForm):

    class Meta:
        model = Relation
        fields = ('date_left',)
        widgets = {'date_left': forms.HiddenInput()}


class UpdatePositionForm(forms.ModelForm):

    class Meta:
        model = Relation
        fields = ('position',)


class ChangePasswordForm(UserCreationForm):

    class Meta:
        model = Member
        fields = ('username', 'password1', 'password2')
        widgets = {'username': forms.HiddenInput()}
