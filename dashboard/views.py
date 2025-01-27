from django.shortcuts import render
from django.contrib.auth.models import User
from base.models import Classe, Topic, Reply, Vote


def dashboard_view(request):
    # Contadores de usuários
    total_users = User.objects.count()
    total_egressos = User.objects.filter(groups__name="Egressos").count()
    total_visitantes = User.objects.filter(groups__name="Visitantes").count()

    # Dados das Classes (antes Sala), Tópicos, Subclasses e Votos
    classes_data = []
    classes = Classe.objects.all()
    for classe in classes:
        total_subclasses = classe.subcategorias.count()  # Contando as subclasses associadas à classe
        total_topics = Topic.objects.filter(subcategoria__classe=classe).count()  # Tópicos associados
        total_replies = Reply.objects.filter(topic__subcategoria__classe=classe).count()  # Respostas associadas
        total_votes = Vote.objects.filter(reply__topic__subcategoria__classe=classe).count()  # Votos associados

        classes_data.append({
            'classe': classe.name,
            'total_subclasses': total_subclasses,
            'total_topics': total_topics,
            'total_replies': total_replies,
            'total_votes': total_votes
        })

    context = {
        'total_users': total_users,
        'total_egressos': total_egressos,
        'total_visitantes': total_visitantes,
        'classes_data': classes_data,
    }
    return render(request, 'dashboard.html', context)
