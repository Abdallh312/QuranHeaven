from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.forms import UserCreationForm
from django_recaptcha.fields import ReCaptchaField 
from django_recaptcha.widgets import ReCaptchaV2Checkbox 
from django.contrib.auth import get_user_model
from tinymce.widgets import TinyMCE

class NewsletterForm(forms.Form):
    subject = forms.CharField()
    receivers = forms.CharField()
    message = forms.CharField(widget=TinyMCE(), label="Email content")
class SignupForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox) 
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='A valid email address, please.', required=True)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return user
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'image', 'description']

class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']

class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username or email '}),
        label="Username ")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))
    capthca=ReCaptchaField(widget=ReCaptchaV2Checkbox)
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'image', 'description']
        

class SeriesCreateForm(forms.ModelForm):
    class Meta:
        model = ArticleSeries

        fields = [
            "title",
            "subtitle",
            "slug",
            "image",
            "video",
        ]
class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article

        fields = [
            "title",
            "subtitle",
            "article_slug",
            "content",
            "notes",
            "series",
            "image",
            "video"
        ]

class SeriesUpdateForm(forms.ModelForm):
    class Meta:
        model = ArticleSeries

        fields = [
            "title",
            "subtitle",
            "image",
            'video',
        ]

class ArticleUpdateForm(forms.ModelForm):
    class Meta:
        model = Article

        fields = [
            "title",
            "subtitle",
            "content",
            "notes",
            "series",
            "image",
            'video'
        ]

class OrderForm(forms.ModelForm):

    class Meta:

        model = order

        fields = ['email', 'phonenumber']

class FatwaForm(forms.Form):
    name = forms.CharField(max_length=100, label="Name", widget=forms.TextInput(attrs={'placeholder': 'Enter your name'}))
    question = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter the questuion'}), label="Question")
    category = forms.CharField(max_length=100, required=False, label="Category",widget=forms.TextInput(attrs={'placeholder': 'Enter the category of questuion'}))
class orderformm(forms.ModelForm):

    class Meta:

        model = orderr

        fields = ['phonenumber', 'email']

class WallEntryForm_100(forms.ModelForm):

    class Meta:

        model = WallEntry_100

        fields = ['wall_number', 'screenshot']
    

class WallEntryForm_200(forms.ModelForm):

    class Meta:

        model = WallEntry_200

        fields = ['wall_number', 'screenshot']