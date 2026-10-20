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

    TIPO_ESCOLHA = [
        ('GERAL', 'Meta Geral'),
        ('INDIVIDUAL', 'Meta Individual:')
    ]
    
    #conexao de metas e empresas
    #o ForeignKey serve pra conectar coisas
    company = models.ForeignKey(
        'accounts.Company',
        on_delete=models.CASCADE,
        related_name='metas',
        verbose_name="Empresa",
    )
    funcionario = models.ForeignKey(
        'accounts.Funcionario',
        on_delete=models.CASCADE,
        related_name='metas',
        null=True,
        blank=True,
        verbose_name="Funcionário Responsável",
    )

    
    # Adicionado o campo 'tipo' usando TIPO_ESCOLHA
    tipo = models.CharField(max_length=10, choices=TIPO_ESCOLHA, default='GERAL', verbose_name="Tipo de Meta")#tipo de meta
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='metas')#quem criou
    nome = models.CharField(max_length=255)#nome da meta
    pilar_esg = models.CharField(max_length=1, choices=ESG_ESCOLHA)#pilar ESG
    deadline = models.DateField()#Quanto tempo dura a meta
    resumo = models.TextField()#resumo da meta
    prioridade = models.CharField(max_length=5, choices=NIVEL_PRIORIDADE, default='MEDIA')#nivel de prioridade
    completo = models.BooleanField(default=False)#statuts da meta
    data_criacao = models.DateTimeField(auto_now_add=True)#quando foi criado

    def __str__(self):
        if self.tipo == 'INDIVIDUAL' and self.funcionario:
            return f"{self.nome} - {self.funcionario.user.username} [{self.pilar_esg}]"
        return f"{self.nome} - Meta Geral [{self.pilar_esg}]"

    
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