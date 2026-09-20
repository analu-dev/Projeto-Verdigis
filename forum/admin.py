from django.contrib import admin
from .models import (
    SecaoConteudo, MembroEquipe, Pilar, 
    ItemLista, Tecnologia, PraticaFarmacia, Contato
)

# PÁGINAS INSTITUCIONAIS E CONTEÚDO

@admin.register(SecaoConteudo)
class SecaoConteudoAdmin(admin.ModelAdmin):
    list_display = ('pagina', 'titulo', 'ordem')
    list_filter = ('pagina',)
    search_fields = ('titulo', 'texto')
    list_editable = ('ordem',) 


@admin.register(MembroEquipe)
class MembroEquipeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'curso', 'ordem', 'ativo')
    list_filter = ('ativo', 'curso')
    search_fields = ('nome', 'email', 'curso')
    list_editable = ('ordem', 'ativo')


@admin.register(ItemLista)
class ItemListaAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'texto_curto', 'ordem')
    list_filter = ('categoria',)
    search_fields = ('texto',)
    list_editable = ('ordem',)

    def texto_curto(self, obj):
        return obj.texto[:60] + '...' if len(obj.texto) > 60 else obj.texto
    texto_curto.short_description = 'Texto do Item'


@admin.register(Tecnologia)
class TecnologiaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ordem')
    search_fields = ('nome', 'descricao')
    list_editable = ('ordem',)

# MÓDULO ESG / FARMÁCIA (COM INLINE)

class PraticaFarmaciaInline(admin.TabularInline):
    model = PraticaFarmacia
    extra = 1


@admin.register(Pilar)
class PilarAdmin(admin.ModelAdmin):
    list_display = ('sigla', 'nome', 'ordem')
    search_fields = ('sigla', 'nome', 'descricao')
    list_editable = ('ordem',)
    inlines = [PraticaFarmaciaInline]


@admin.register(PraticaFarmacia)
class PraticaFarmaciaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'pilar', 'ordem')
    list_filter = ('pilar',)
    search_fields = ('titulo', 'descricao')
    list_editable = ('ordem',)


# CONTATOS E ATENDIMENTO (CRM)

@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'assunto', 'empresa', 'data_envio', 'respondido')
    list_filter = ('respondido', 'assunto', 'data_envio')
    search_fields = ('nome', 'email', 'empresa', 'mensagem')
    list_editable = ('respondido',) 
    date_hierarchy = 'data_envio' 
    
    readonly_fields = ('nome', 'email', 'empresa', 'assunto', 'mensagem', 'data_envio')
