from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelChoiceField

from relation.models import Member, DeliveryCenter


class AddMemberForm(UserCreationForm):
    username = forms.CharField(max_length=255, help_text='Required. Inform a valid username.')
    email = forms.EmailField(max_length=50, help_text='Required. Inform a valid email address.')
    delivery_center = ModelChoiceField(queryset=DeliveryCenter.objects.all())

    class Meta:
        model = Member
        fields = ('username', 'email', 'delivery_center', 'password1', 'password2')


class EmailLoginForm(AuthenticationForm):
    username = UsernameField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': ''}),
        label='Email')

    def clean(self):
        try:
            self.cleaned_data["username"] = get_user_model().objects.get(email=self.data["username"])
        except ObjectDoesNotExist:
            self.cleaned_data["username"] = "a_username_that_do_not_exists_anywhere_in_the_site"
        return super(EmailLoginForm, self).clean()
