from django import forms
from .models import Todo
from django.forms import ModelForm

class LoginForm(forms.Form):
    username = forms.CharField(label="username")
    password = forms.CharField(label="password", widget=forms.PasswordInput())

class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ["task"]
