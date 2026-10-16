from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Meta
from .forms import FormsMetas
from django.shortcuts import render
from django.db.models import Count
from .models import RelatoSocialVerdigis



@login_required
def home(request):
    """Página inicial da área logada. Acesso restrito a usuários autenticados."""
    return render(request, 'dashboard/dashboard.html')

#Fabrica de metas
@login_required
def fabrica_metas_view(request):
    metas = Meta.objects.filter(usuario=request.user)
    
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
    meta.save()
    return redirect('dashboard:fabrica_metas')

@login_required
@require_POST
def deletar_meta_view(request, meta_id):
    meta = get_object_or_404(Meta, id=meta_id, usuario=request.user)
    meta.delete()
    return redirect('dashboard:fabrica_metas')

def dashboard_social_verdigis(request):
    
    filtro_sentimento = request.GET.get('sentimento')
    relatos = RelatoSocialVerdigis.objects.all()
    
    if filtro_sentimento:
        relatos = relatos.filter(sentimento=filtro_sentimento)

    metricas_por_tema = relatos.values('tema_esg').annotate(
        total_relatos=Count('id')
    ).order_by('-total_relatos')

    alertas_criticos = RelatoSocialVerdigis.objects.filter(sentimento='NEGATIVO').count()

    context = {
        'relatos': relatos,
        'metricas_por_tema': metricas_por_tema,
        'alertas_criticos': alertas_criticos,
    }
    
    return render(request, 'dashboard/avaliacao.html', context)