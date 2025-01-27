from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone


# Modelo para Classe
class Classe(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    grupos_permitidos = models.ManyToManyField(Group, blank=True, related_name='classes')
    usuarios_permitidos = models.ManyToManyField(User, blank=True, related_name='classes')
    publico = models.BooleanField(default=True)  # Define se é acessível a todos ou não

    def __str__(self):
        return self.name


# Modelo para SubCategoria (associada a Classe)
class SubCategoria(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='subcategorias')

    def __str__(self):
        return self.name


# Modelo para Tag (associada a Tópicos)
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# Modelo para Tópico
class Topic(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE, related_name='topics')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, related_name="topics", blank=True)  # Adicione `blank=True` para aceitar tópicos sem tags
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Modelo para Resposta
class Reply(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default=0)  # Contador de votos

    def __str__(self):
        return f"Reply to {self.topic.title}"


# Modelo para Voto
class Vote(models.Model):  # Voto para Resposta
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    reply = models.ForeignKey(Reply, related_name='vote_set', on_delete=models.CASCADE)  # Alterado related_name
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'reply')

    def __str__(self):
        return f"Vote by {self.user.username if self.user else 'Unknown'} on reply {self.reply.id}"

