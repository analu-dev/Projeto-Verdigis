from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from accounts.models import UserProfile

User = get_user_model()


class SignupForm(UserCreationForm):
    email = forms.EmailField(label='E-mail')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Digite seu nome de usuário'
        self.fields['email'].widget.attrs['placeholder'] = 'seuemail@exemplo.com'
        self.fields['password1'].widget.attrs['placeholder'] = 'Crie uma senha'
        self.fields['password2'].widget.attrs['placeholder'] = 'Repita a senha'

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Já existe uma conta cadastrada com este e-mail.')
        return email


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['username'].widget.attrs['placeholder'] = 'Digite seu nome de usuário'
            self.fields['password'].widget.attrs['placeholder'] = 'Insira sua senha'
    
    error_messages = {
        'invalid_login': 'Usuário ou senha incorretos.',
        'inactive': 'Esta conta está desativada.',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Digite seu nome de usuário'
        self.fields['password'].widget.attrs['placeholder'] = 'Digite sua senha'

class DeleteAccountForm(forms.Form):
    password = forms.CharField(
        label='Senha',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs['placeholder'] = 'Digite sua senha'

    def clean_password(self):
        password = self.cleaned_data['password']
        if not self.user.check_password(password):
            raise forms.ValidationError('Senha incorreta.')
        return password

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'cnpj', 'email', 'profile_picture']
        labels = {
            'name': 'Nome',
            'cnpj': 'CNPJ',
            'email': 'E-mail',
            'profile_picture': 'Foto de Perfil'
        }

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Digite seu nome'}),
            'cnpj': forms.TextInput(attrs={'placeholder': 'Digite seu CNPJ'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Digite seu e-mail'}),
            'profile_picture': forms.FileInput(attrs={'accept': 'image/*'}),
        }

    