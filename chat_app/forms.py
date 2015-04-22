from django import forms
from django.contrib.auth.forms import UserCreationForm
from models import *

class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(MyRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        # user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        return user

class ProfileUpdate(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This email already in use.')
        return email

    def save(self, commit=True):
        user = super(ProfileUpdate, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class AddContactForm(forms.ModelForm):
    name= forms.CharField(label="UserName")


class UserProfilePicForm(forms.ModelForm):

    class Meta:
        model = UserProfilePic
        fields = ('pic',)

    def save(self, commit=True):
        user = super(UserProfilePicForm, self).save(commit=False )
        if commit:
            user.save()
        return user or None



