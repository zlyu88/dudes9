from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.db import transaction
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
    password1 = forms.CharField(required=False, widget=forms.HiddenInput(), initial='1234qwer')
    password2 = forms.CharField(required=False, widget=forms.HiddenInput(), initial='1234qwer')

    class Meta:
        model = Member
        fields = ('delivery_center', 'username', 'email', 'image')

    def send_password(self, password):
        data = {'username': self.cleaned_data["username"],
                'password': password}
        subject = 'Dudes9 temporary password'
        body = 'Hi, {username}.\nHere is your temporary password for dudes9 {password}.\n' \
               'Please login and change it you like.'.format(**data)
        email = EmailMessage(subject, body, to=[self.cleaned_data["email"]])
        email.send()

    def save(self, commit=True):
        user = super(AddMemberForm, self).save(commit=False)
        password = Member.objects.make_random_password()
        user.set_password(password)
        if commit:
            user.save()
            self.send_password(password)
        return user


class AddProjectForm(forms.ModelForm):
    title = forms.CharField(max_length=255, help_text='Required. Inform a valid project title.')
    technologies = ModelMultipleChoiceField(queryset=Technology.objects.all())

    class Meta:
        model = Relation
        fields = ('title', 'technologies')

    @transaction.atomic
    def save(self, **kwargs):
        data = self.cleaned_data
        project = Project(title=data['title'], start_date=str(timezone.now()))
        project.save()
        project.technologies.add(*[tech for tech in data['technologies']])
        return project


class AddRelationForm(forms.ModelForm):
    member = ModelChoiceField(queryset=Member.objects.all(), help_text='Required. Inform a valid member.')
    project = ModelChoiceField(queryset=Project.objects.filter(end_date=None), help_text='Required. Inform a valid project.')

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


class ChangePasswordForm(PasswordChangeForm):

    class Meta:
        model = Member
        fields = ('old_password', 'new_password1', 'new_password2')


class AddTechnologyForm(forms.ModelForm):
    title = forms.CharField(max_length=255, help_text='Required. Inform a valid technology title.')

    class Meta:
        model = Technology
        fields = ('title',)
