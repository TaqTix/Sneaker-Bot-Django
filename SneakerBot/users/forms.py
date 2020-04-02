from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import WebProfile, NikeTestBackEnd

class ProfileCreatorForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("username", "password")


class NikeTaskForm(forms.ModelForm):
    class Meta:
        model = NikeTestBackEnd
        fields = [
            'url',
            'size',
            'username',
            'password',
        ]
    
    def save(self, commit=True):
        task = super(NikeTaskForm, self).save(commit=False)
        task.url = self.cleaned_data["url"]
        task.size = self.cleaned_data["size"]
        task.username = self.cleaned_data["username"]
        task.password = self.cleaned_data["password"]

        if commit:
            task.save()
        return task
        #nowhere near finished

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    receive_email_promotions = forms.BooleanField(required=False, initial=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "receive_email_promotions")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.receive_email_promotions = self.cleaned_data["receive_email_promotions"]
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

class WebsiteProfileForm(forms.ModelForm):

    class Meta:
        model = WebProfile
        fields = ['username', 'password']

    # def __init__(self, *args, **kwargs):
    #     super(UserCreationForm, self).__init__(*args, **kwargs)
    #     self.fields['id_username'].widget.attrs['cols'] = 10;