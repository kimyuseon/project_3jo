from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SignUpForm(forms.ModelForm):
    username = forms.CharField(label='아이디', help_text='')
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput())
    password_confirm = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm:
            if password != password_confirm:
                raise ValidationError("비밀번호가 일치하지 않습니다.")
        
        return cleaned_data