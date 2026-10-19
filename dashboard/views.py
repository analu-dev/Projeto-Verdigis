from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import FormsMetas
from .models import Meta, RelatoSocialVerdigis


from django.utils import timezone

@login_required
def home(request):
    metas = Meta.objects.filter(usuario=request.user)
    return render(request, 'dashboard/dashboard.html', {
        'metas_atrasadas': metas.filter(completo=False, deadline__lt=timezone.localdate()).count(),
        'metas_concluidas': metas.filter(completo=True).count(),
    })



#Fabrica de metas
@login_required
def fabrica_metas_view(request):
    metas = Meta.objects.filter(usuario=request.user).order_by('completo', 'deadline')

    if request.method == 'POST':
        form = FormsMetas(request.POST)
        if form.is_valid():
            meta = form.save(commit=False)
            meta.usuario = request.user
            meta.save()
            return redirect('dashboard:fabrica_metas')
    else:
        form = FormsMetas()

    return render(request, 'dashboard/fabrica_metas.html', {
        'metas': metas,
        'form': form,
        'hoje': timezone.localdate(),
    })


@login_required
def editar_meta_view(request, meta_id):
    meta = get_object_or_404(Meta, id=meta_id, usuario=request.user)

    if request.method == 'POST':
        form = FormsMetas(request.POST, instance=meta) #instace == atualizar
        if form.is_valid():
            form.save()
            return redirect('dashboard:fabrica_metas')
    else:
        form = FormsMetas(instance=meta)

    return render(request, 'dashboard/editar_meta.html', {
        'form': form,
        'meta': meta,
    })


@login_required
@require_POST
def alternar_conclusao_view(request, meta_id):
    meta = get_object_or_404(Meta, id=meta_id, usuario=request.user)
    # Inverte o estado atual (se era False vira True, e vice-versa)
    meta.completo = not meta.completo
    meta.save(update_fields=['completo'])
    return redirect('dashboard:fabrica_metas')


@login_required
@require_POST
def deletar_meta_view(request, meta_id):
    meta = get_object_or_404(Meta, id=meta_id, usuario=request.user)
    meta.delete()
    return redirect('dashboard:fabrica_metas')


@login_required
def dashboard_social_verdigis(request):
    tema = request.GET.get('tema', '')
    sentimento = request.GET.get('sentimento', 'NEGATIVO')
    if sentimento not in ('POSITIVO', 'NEGATIVO', 'NEUTRO'):
        sentimento = 'NEGATIVO'

    contagem = {
        m['tema_esg']: m['total']
        for m in RelatoSocialVerdigis.objects.values('tema_esg').annotate(total=Count('id'))
    }
    nomes = dict(RelatoSocialVerdigis.TEMA_ESG_CHOICES)
    temas = [
        {'codigo': codigo, 'nome': nome, 'total': contagem.get(codigo, 0)}
        for codigo, nome in RelatoSocialVerdigis.TEMA_ESG_CHOICES
    ]

    relatos = RelatoSocialVerdigis.objects.filter(sentimento=sentimento).order_by('-data_registro')
    if tema in nomes:
        relatos = relatos.filter(tema_esg=tema)
    else:
        tema = ''

    return render(request, 'dashboard/avaliacao.html', {
        'relatos': relatos,
        'temas': temas,
        'tema_atual': tema,
        'tema_atual_nome': nomes.get(tema, ''),
        'sentimento_atual': sentimento,
    })


@login_required
def detalhe_relato_view(request, relato_id):
    relato = get_object_or_404(RelatoSocialVerdigis, id=relato_id)
    return render(request, 'dashboard/avaliacao_detalhe.html', {'relato': relato})