from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import DeleteAccountForm, LoginForm, ProfileForm, SignupForm
from .models import UserProfile


def _dados_post(request):
    return request.POST if request.method == 'POST' else None


def signup(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    form = SignupForm(_dados_post(request))
    if form.is_valid():
        user = form.save()
        auth.login(request, user)
        messages.success(request, 'Conta criada com sucesso.')
        return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, 'accounts/signup.html', {'form': form})


def login(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    next_url = request.POST.get('next') or request.GET.get('next', '')
    form = LoginForm(request, data=_dados_post(request))
    if form.is_valid():
        auth.login(request, form.get_user())
        destino_seguro = url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        )
        return redirect(next_url if destino_seguro else settings.LOGIN_REDIRECT_URL)

    return render(request, 'accounts/login.html', {'form': form, 'next': next_url})


@require_POST
def logout(request):
    auth.logout(request)
    messages.success(request, 'Você saiu da sua conta.')
    return redirect(settings.LOGOUT_REDIRECT_URL)


@login_required
def delete(request):
    form = DeleteAccountForm(request.user, _dados_post(request))
    if form.is_valid():
        user = request.user
        auth.logout(request)
        user.delete()
        messages.success(request, 'Sua conta foi excluída.')
        return redirect(settings.LOGOUT_REDIRECT_URL)

    return render(request, 'accounts/delete.html', {'form': form})

@login_required
def profile(request):
    profile_obj, _ = UserProfile.objects.get_or_create(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile_obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, 'Perfil atualizado com sucesso.')
        return redirect('profile')

    return render(request, 'accounts/profile.html', {'form': form})
