from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from users.models import User
from captcha.fields import CaptchaField


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Введите имя пользователя"
        }))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Введите пароль"
        }))

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control py-4"

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите имя'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите фамилию'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите имя пользователя'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Введите адрес электронной почты'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Подтвердите пароль'}))

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control py-4"

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'readonly': True}))
    image = forms.ImageField(widget=forms.FileInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control py-4"
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'image')


class ContactForm(forms.Form):
    name = forms.CharField(
        label='Имя',
        min_length=3,
        max_length=200,
        widget=forms.TextInput(
            attrs={'placeholder': 'Ваше имя',
                   'class': 'form-input'}
        )
    )
    email = forms.EmailField(
        label='e-mail',
        widget=forms.EmailInput(
            attrs={'placeholder': 'Электронная почта'}
        )
    )
    message = forms.CharField(
        label='Сообщение',
        min_length=20,
        widget=forms.Textarea(
            attrs={'placeholder': 'Сообщение',
                   'cols': 30, 'rows': 9}
        )
    )
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control py-4"

    class Meta:
        model = User
        fields = ('name', 'email', 'message', 'captcha')
