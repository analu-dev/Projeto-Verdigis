from django.conf import settings
from django.db import models

#fabrica de metas!!
class Meta(models.Model):
    ESG_ESCOLHA = [
        ('E', 'Ambiental (Environmental)'),
        ('S', 'Social'),
        ('G', 'Governança (Governance)')
    ]

    NIVEL_PRIORIDADE = [
        ('BAIXA', 'Baixa'),
        ('MEDIA', 'Média'),
        ('ALTA', 'Alta')
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='metas'
    )
    nome = models.CharField(max_length=255)
    tipo_esg = models.CharField(max_length=1, choices=ESG_ESCOLHA)
    deadline = models.DateField()
    resumo = models.TextField()
    prioridade = models.CharField(max_length=5, choices=NIVEL_PRIORIDADE, default='MEDIA')
    completo = models.BooleanField(default=False)
    criador = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - [{self.tipo_esg}]"
    
#Quadro de avaliações

class RelatoSocialVerdigis(models.Model):
    TEMA_ESG_CHOICES = [
        ('SAUDE_MENTAL', 'Saúde Mental e Bem-estar'),
        ('DIVERSIDADE', 'Diversidade, Equidade e Inclusão'),
        ('SEGURANCA', 'Saúde e Segurança do Trabalho'),
        ('LIDERANCA', 'Práticas de Liderança e Gestão'),
        ('BENEFICIOS', 'Remuneração e Benefícios'),
    ]
    
    IMPACTO_CHOICES = [
        ('POSITIVO', 'Impacto Positivo (Elogio/Boa Prática)'),
        ('NEGATIVO', 'Impacto Negativo (Reclamação/Risco)'),
        ('NEUTRO', 'Neutro (Sugestão/Dúvida)'),
    ]

    mensagem = models.TextField(help_text="Relato ou avaliação do colaborador")
    tema_esg = models.CharField(max_length=20, choices=TEMA_ESG_CHOICES)
    sentimento = models.CharField(max_length=10, choices=IMPACTO_CHOICES)
    data_registro = models.DateTimeField(auto_now_add=True)
    
    eh_anonimo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Relato Social ESG"
        verbose_name_plural = "Relatos Sociais ESG"

    def __str__(self):
        return f"Relato {self.get_tema_esg_display()} - {self.get_sentimento_display()}"