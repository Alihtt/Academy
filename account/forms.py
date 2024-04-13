from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.core.exceptions import ValidationError
from .models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='رمز', widget=forms.PasswordInput())
    password2 = forms.CharField(
        label='تکرار رمز', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('phone_number', 'email', 'first_name', 'last_name')

    def clean_password2(self):
        cd = self.cleaned_data

        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('Your passwords must match')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('phone_number', 'first_name', 'last_name', 'email')
        labels = {
            "phone_number": _("تلفن همراه"),
            "first_name": _("نام"),
            'last_name': _("نام خانوادگی"),
            'email': _("ایمیل"),
        }
        widgets = {
            'phone_number': forms.TextInput(attrs={'readonly': 'readonly'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name'), Column('last_name')
            ),
            'email',
            'phone_number',
            Submit('submit', 'ذخیره', css_class='my-1'),

        )


class UserLoginForm(forms.Form):
    phone_number = forms.CharField(
        label="تلفن همراه", widget=forms.TextInput({"class": "border-start-0 form-control ms-0"}),
    )
    password = forms.CharField(
        label="رمز عبور", widget=forms.PasswordInput({"class": "border-start-0 form-control ms-0"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'phone_number',
            'password',
            Submit('submit', 'ورود')
        )
