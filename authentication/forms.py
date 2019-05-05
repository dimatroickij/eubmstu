from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, PasswordChangeForm, \
    SetPasswordForm
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget

from authentication.models import User


class LoginForm(AuthenticationForm):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        UserModel = get_user_model()
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control'})
        captcha = ReCaptchaField(widget=ReCaptchaWidget())
        # self.username_field = 'username'
        self.fields['username'].label = 'Логин'
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})

    class Meta:
        model = User
        fields = ('username', 'password')


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Обязательное поле',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['first_name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['last_name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['patronymic'].widget = forms.TextInput(attrs={'class': 'form-control'})

    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'patronymic', 'email', 'password1', 'password2')


class MyPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control'})

    class Meta:
        model = User
        fields = ('email')


class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget = widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['new_password1'].widget = widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['new_password2'].widget = widget = forms.PasswordInput(attrs={'class': 'form-control'})

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


class MySetPasswordForm(SetPasswordForm):
    # new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget = widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['new_password2'].widget = widget = forms.PasswordInput(attrs={'class': 'form-control'})

    class Meta:
        model = User
        fields = ('new_password1', 'new_password2')
