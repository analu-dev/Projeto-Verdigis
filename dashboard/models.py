from django.db import models
from django.contrib.auth.models import User

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

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metas')
    nome = models.CharField(max_length=255)
    tipo_esg = models.CharField(max_length=1, choices=ESG_ESCOLHA)
    deadline = models.DateField()
    resumo = models.TextField()
    prioridade = models.CharField(max_length=5, choices=NIVEL_PRIORIDADE, default='MEDIA')
    completo = models.BooleanField(default=False)
    criador = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - [{self.tipo_esg}]"
