import django.forms as forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory

from .models import Client, Schedule


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password", "first_name", "last_name"]
        widgets = {
            "password": forms.TextInput(attrs={"type":"password"})
        }
        exclude = None


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = "__all__"
        exclude = ("user", )
        widgets = {
            "password": forms.PasswordInput(),
            "cpf": forms.TextInput(attrs={"class": "cpf"}),
        }


class ClientLoginForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ClientLoginForm, self).__init__(*args, **kwargs)
        self.fields["nickname"].label = ""
        self.fields["password"].label = ""

    class Meta:
        model = User
        fields = ["username", "password"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control mb-4", "placeholder": "nickname"}),
            "password": forms.PasswordInput(attrs={"class": "form-control", "placeholder": "senha"}),
        }


class ScheduleRegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ScheduleRegisterForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Schedule
        fields = ["service", "date"]
        widgets = {
            "date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


ClientFormset = inlineformset_factory(User, Client, fields="__all__")
