from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.email_error = ''

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def is_valid(self):
        isvalid = super(RegistrationForm, self).is_valid()
        try:
            valid_email = not User.objects.filter(email=self.cleaned_data["email"])
            if not valid_email:
                self.email_error = 'The email is already in use.'
                return
            else:
                return isvalid and valid_email
        except KeyError:
            self.email_error = 'Please enter an email address'
            return

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class EditProfileForm(UserChangeForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")

    def is_valid(self, user):
        isvalid = super(EditProfileForm, self).is_valid()
        try:
            valid_email = not User.objects.filter(email=self.cleaned_data["email"]) \
                .exclude(username=user.username)
            if not valid_email:
                self.email_error = 'The email is already in use.'
                return
            else:
                return isvalid and valid_email
        except KeyError:
            self.email_error = 'Please enter an email address'
            return
