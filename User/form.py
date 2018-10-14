from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email1 = forms.EmailField(required=True)
    email2 = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("first_name",
                  "last_name",
                  "username",
                  "email1",
                  "email2",
                  "password1",
                  "password2")

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email1"]
        if commit:
            user.save()
        return user

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not (all(x.isalpha() or x.isspace() for x in first_name)):
            raise forms.ValidationError(
                'Enter alphabetical characters and spaces only.'
            )
        if len(first_name) > 20:
            raise forms.ValidationError(
                'Name must contain 20 characters or less.'
            )
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if not (all(x.isalpha() or x.isspace() for x in last_name)):
            raise forms.ValidationError(
                'Enter alphabetical characters and spaces only.'
            )
        if len(last_name) > 20:
            raise forms.ValidationError(
                'Name must contain 20 characters or less.'
            )
        return last_name

    def clean_email2(self):
        email1 = self.cleaned_data.get("email1")
        email2 = self.cleaned_data.get("email2")
        if email1 and email2 and email1 != email2:
            raise forms.ValidationError(
                'Emails do not match.'
            )
        else:
            inuse = not User.objects.filter(email=self.cleaned_data["email2"])
            if not inuse:
                raise forms.ValidationError(
                    'Email is already in use.'
                )
        return email2
