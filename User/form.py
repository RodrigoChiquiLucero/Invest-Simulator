from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions



class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email1 = forms.EmailField(required=True)
    email2 = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)

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
                'First name must contain 20 characters or less.'
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
                'Last name must contain 20 characters or less.'
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


class EditProfileForm(UserChangeForm):
    email = forms.EmailField(required=True)
    image = forms.ImageField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "image")

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

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            w, h = get_image_dimensions(avatar)

            # validate dimensions
            max_width = max_height = 100
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                    '%s x %s pixels or smaller.' % (max_width, max_height))

            # validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, GIF or PNG image.')

            # validate file size
            if len(avatar) > (20 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 20k.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar
