from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import (
    SecaoConteudo,
    MembroEquipe,
    Pilar,
    ItemLista,
    Tecnologia,
    PraticaFarmacia,
    Contato
)


def index(request):
    secoes = SecaoConteudo.objects.filter(pagina=SecaoConteudo.PAGINA_INDEX)
    pilares = Pilar.objects.prefetch_related('praticas').all()

    context = {
        'secoes': secoes,
        'pilares': pilares,
    }
    return render(request, 'forum/index.html', context)


def quem_somos(request):
    secoes = SecaoConteudo.objects.filter(pagina=SecaoConteudo.PAGINA_QUEM_SOMOS)
    membros = MembroEquipe.objects.filter(ativo=True)

    context = {
        'secoes': secoes,
        'membros': membros,
    }
    return render(request, 'forum/quem_somos.html', context)


def sobre_projeto(request):
    secoes = SecaoConteudo.objects.filter(pagina=SecaoConteudo.PAGINA_SOBRE_PROJETO)
    
    objetivos = ItemLista.objects.filter(categoria=ItemLista.CATEGORIA_OBJETIVO)
    praticas_fds = ItemLista.objects.filter(categoria=ItemLista.CATEGORIA_PRATICA_FDS)
    beneficios = ItemLista.objects.filter(categoria=ItemLista.CATEGORIA_BENEFICIO)
    
    tecnologias = Tecnologia.objects.all()
    pilares = Pilar.objects.prefetch_related('praticas').all()

    context = {
        'secoes': secoes,
        'objetivos': objetivos,
        'praticas_fds': praticas_fds,
        'beneficios': beneficios,
        'tecnologias': tecnologias,
        'pilares': pilares,
    }
    return render(request, 'forum/sobre_projeto.html', context)


def fale_conosco(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        empresa = request.POST.get('empresa', '')
        assunto = request.POST.get('assunto')
        mensagem = request.POST.get('mensagem')

        if nome and email and mensagem:
            Contato.objects.create(
                nome=nome,
                email=email,
                empresa=empresa,
                assunto=assunto,
                mensagem=mensagem,
                data_envio=timezone.now()
            )
            messages.success(request, 'Sua mensagem foi enviada com sucesso! Entraremos em contato em breve.')
            return redirect('fale_conosco')
        else:
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')

    assunto_choices = Contato.ASSUNTO_CHOICES

    context = {
        'assunto_choices': assunto_choices,
    }
    return render(request, 'forum/fale_conosco.html', context)