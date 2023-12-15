from django import forms
from django.forms import ModelForm, TextInput, PasswordInput, DateInput

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from main_app.models import User, SupportRequest


class AuthUserForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}))


class UpdUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email',

                  'first_name',
                  'last_name',
                  # 'document_id',
                  'position',
                  # 'avatar'
                  'birth_date',
                  'user_phone_num',
                  'groups',

                  ]
        widgets = {

            "birth_date": DateInput(attrs={
                # 'class': 'form-control',
                'placeholder': 'День рождения',
                'type': 'date'
            }),

        }


class AddUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email',
                  'password1',
                  'password2',
                  'first_name',
                  'last_name',
                  # 'document_id',
                  'position',
                  # 'avatar'
                  'is_boss',
                  'birth_date',
                  'user_phone_num',
                  'groups',

                  ]
        widgets = {

            "birth_date": DateInput(attrs={
                # 'class': 'form-control',
                'placeholder': 'День рождения',
                'type': 'date'
            }),

        }


class SupportRequestForm(forms.ModelForm):
    class Meta:
        model = SupportRequest
        fields = ['request_theme', 'about']

        widgets = {
            'request_theme': forms.TextInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control'}),
            # 'request_from': forms.Select(attrs={'class': 'form-control'}),
            # 'is_done': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
