from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from Game.models import Wallet
from django.core.files.images import get_image_dimensions


def clean_name(name):
    if not (all(x.isalpha() or x.isspace() for x in name)):
        raise forms.ValidationError(
            'Enter alphabetical characters and spaces only.'
        )
    if len(name) > 20:
        raise forms.ValidationError(
            'First name must contain 20 characters or less.'
        )
    return name


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
        # asign a wallet
        wallet = Wallet(user=user)
        wallet.save()
        if commit:
            user.save()
        return user

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        return clean_name(first_name)

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        return clean_name(last_name)

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
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ("first_name",
                  "last_name",
                  "email")

    def clean_email(self):
        email = self.cleaned_data['email']
        if email and User.objects.filter(email=email) \
                .exclude(username=self.instance.username):
            raise forms.ValidationError(
                'Email is already in use.'
            )
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        return clean_name(first_name)

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        return clean_name(last_name)


class AvatarForm(forms.Form):
    avatar = forms.ImageField(required=True)

    def setUser(self, user):
        self.user = user

    class Meta:
        model = User
        fields = "avatar"

    def clean_avatar(self):
        avatar = self.cleaned_data["avatar"]
        try:
            w, h = get_image_dimensions(avatar)
            # validate dimensions
            max_width = max_height = 900
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
            pass

        return avatar

    def save(self):
        wallet = Wallet.objects.get(user=self.user)
        wallet.image = self.cleaned_data["avatar"]
        wallet.save()
