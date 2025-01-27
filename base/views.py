from django.shortcuts import render, redirect, get_object_or_404
from .models import Classe, SubCategoria, Topic, Reply, Vote, Tag
from .forms import ClasseForm, SubCategoriaForm, TopicForm, ReplyForm, TagForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
#----------------------------------------------------------------------------------------
from django.http import HttpResponseForbidden

def check_access_to_classe(request, classe):
    if not classe.publico:
        # Verifica se o usuário tem permissão (usuários permitidos ou grupos permitidos)
        if request.user not in classe.usuarios_permitidos.all() and not classe.grupos_permitidos.filter(id__in=request.user.groups.values_list('id', flat=True)).exists():
            return HttpResponseForbidden("Você não tem permissão para acessar esta classe.")
    return None

# Listar classes com filtro de acesso
from django.db.models import Q

def classe_list(request):
    if request.user.is_authenticated:
        # Filtra classes públicas
        classes_publicas = Classe.objects.filter(publico=True)

        # Filtra classes onde o usuário tem permissão
        classes_com_permissao = Classe.objects.filter(
            Q(usuarios_permitidos=request.user) | 
            Q(grupos_permitidos__in=request.user.groups.all())
        ).distinct()

        # Combine as duas listas manualmente
        classes = list(classes_publicas) + list(classes_com_permissao)

        # Se não houver classes disponíveis, exiba uma mensagem
        if not classes:
            messages.error(request, "Você não tem permissão para acessar nenhuma sala.")
            return redirect('home')  # Redireciona para a página inicial ou outra página

    else:
        # Apenas classes públicas para usuários não autenticados
        classes = Classe.objects.filter(publico=True)

    return render(request, 'classes/classe_list.html', {'classes': classes})


# Criar nova classe (apenas para administradores)
@login_required
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.groups.filter(name="Moderadores").exists()))
def create_classe(request):
    if request.method == 'POST':
        form = ClasseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('classe_list')
    else:
        form = ClasseForm()
    return render(request, 'classes/create_classe.html', {'form': form})

# Editar classe (apenas para administradores)
@login_required
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.groups.filter(name="Moderadores").exists()))
def edit_classe(request, classe_id):
    classe = get_object_or_404(Classe, id=classe_id)
    access_error = check_access_to_classe(request, classe)
    if access_error:
        return access_error

    if request.method == 'POST':
        form = ClasseForm(request.POST, instance=classe)
        if form.is_valid():
            form.save()
            return redirect('classe_list')
    else:
        form = ClasseForm(instance=classe)
    return render(request, 'classes/edit_classe.html', {'form': form})

# Excluir classe (apenas para administradores)
@login_required
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.groups.filter(name="Moderadores").exists()))
def delete_classe(request, classe_id):
    classe = get_object_or_404(Classe, id=classe_id)
    access_error = check_access_to_classe(request, classe)
    if access_error:
        return access_error

    classe.delete()
    return redirect('classe_list')

#----------------------------------------------------------------------------------------

# Views para SubCategoria
def subcategoria_list(request, classe_id):
    classe = get_object_or_404(Classe, id=classe_id)
    subcategorias = SubCategoria.objects.filter(classe=classe)
    return render(request, 'subcategorias/subcategoria_list.html', {'classe': classe, 'subcategorias': subcategorias})

@login_required
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.groups.filter(name="Moderadores").exists()))
def create_subcategoria(request, classe_id):
    classe = get_object_or_404(Classe, id=classe_id)  # Recupera a classe associada pelo ID
    if request.method == 'POST':
        form = SubCategoriaForm(request.POST)
        if form.is_valid():
            subcategoria = form.save(commit=False)  # Não salva ainda, pois precisamos ajustar o campo 'classe'
            subcategoria.classe = classe  # Associa a classe ao objeto
            subcategoria.save()  # Agora sim, salva o objeto com a classe associada
            return redirect('subcategoria_list', classe_id=classe.id)
    else:
        form = SubCategoriaForm()  # Apenas inicializa o formulário sem o campo classe
    return render(request, 'subcategorias/create_subcategoria.html', {'form': form, 'classe': classe})


@login_required
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.groups.filter(name="Moderadores").exists()))
def edit_subcategoria(request, subcategoria_id):
    subcategoria = get_object_or_404(SubCategoria, id=subcategoria_id)
    classe = subcategoria.classe  # Obtém a classe associada à subcategoria
    if request.method == 'POST':
        form = SubCategoriaForm(request.POST, instance=subcategoria)
        if form.is_valid():
            form.save()
            return redirect('subcategoria_list', classe_id=classe.id)  # Redireciona para a lista de subcategorias dessa classe
    else:
        form = SubCategoriaForm(instance=subcategoria)
    
    # Passa tanto a subcategoria quanto a classe para o template
    return render(request, 'subcategorias/edit_subcategoria.html', {'form': form, 'subcategoria': subcategoria, 'classe': classe})


@login_required
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.groups.filter(name="Moderadores").exists()))
def delete_subcategoria(request, subcategoria_id):
    subcategoria = get_object_or_404(SubCategoria, id=subcategoria_id)
    classe_id = subcategoria.classe.id
    subcategoria.delete()
    return redirect('subcategoria_list', classe_id=classe_id)

#----------------------------------------------------------------------------------------

# Views para Topic
def topic_list(request, subcategoria_id):
    subcategoria = get_object_or_404(SubCategoria, id=subcategoria_id)
    topics = Topic.objects.filter(subcategoria=subcategoria).order_by('-created_at')
    tags = Tag.objects.filter(topics__subcategoria=subcategoria).distinct()  # Filtra as tags associadas à subcategoria
    return render(request, 'topics/topic_list.html', {'subcategoria': subcategoria, 'topics': topics, 'tags': tags})

def topic_detail(request, topic_id):
    # Obtém o tópico especificado pelo ID
    topic = get_object_or_404(Topic, id=topic_id)
    
    # Obtém as respostas associadas ao tópico, ordenadas por votos e data de criação
    replies = topic.replies.all().order_by('-votes', '-created_at')

    # Exibindo as tags associadas ao tópico
    tags = topic.tags.all()

    return render(request, 'topics/topic_detail.html', {
        'topic': topic,
        'replies': replies,
        'tags': tags,  # Passa as tags para o template
    })

@login_required
def create_topic(request, subcategoria_id):
    subcategoria = get_object_or_404(SubCategoria, id=subcategoria_id)
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.subcategoria = subcategoria
            topic.author = request.user
            topic.save()  # Primeiro salva o tópico
            # Associa as tags selecionadas ao tópico
            topic.tags.set(form.cleaned_data['tags'])  # Atualiza as tags do tópico
            return redirect('topic_list', subcategoria_id=subcategoria.id)
    else:
        form = TopicForm()
    return render(request, 'topics/create_topic.html', {'form': form, 'subcategoria': subcategoria})

@login_required
def edit_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    # Verifica se o usuário é o autor do tópico
    if request.user != topic.author:
        return redirect('topic_detail', topic_id=topic.id)

    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.save()
            topic.tags.set(form.cleaned_data['tags'])  # Atualiza as tags associadas
            return redirect('topic_detail', topic_id=topic.id)
    else:
        # Inicializa o formulário com as tags associadas ao tópico
        form = TopicForm(instance=topic)

    return render(request, 'topics/edit_topic.html', {
        'form': form,
        'topic': topic
    })

@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.user != topic.author:
        return redirect('topic_detail', topic_id=topic.id)
    subcategoria_id = topic.subcategoria.id
    topic.delete()
    return redirect('topic_list', subcategoria_id=subcategoria_id)

#----------------------------------------------------------------------------------------

# Views para Reply
@login_required
def add_reply(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.topic = topic
            reply.author = request.user
            reply.save()
            return redirect('topic_detail', topic_id=topic.id)
    else:
        form = ReplyForm()
    return render(request, 'replies/add_reply.html', {'form': form, 'topic': topic})

@login_required
def edit_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)
    if request.user != reply.author:
        return redirect('topic_detail', topic_id=reply.topic.id)

    if request.method == 'POST':
        form = ReplyForm(request.POST, instance=reply)
        if form.is_valid():
            form.save()
            return redirect('topic_detail', topic_id=reply.topic.id)
    else:
        form = ReplyForm(instance=reply)
    return render(request, 'replies/edit_reply.html', {'form': form, 'reply': reply})

@login_required
def vote_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)

    try:
        vote = Vote.objects.get(user=request.user, reply=reply)
        vote.delete()
        reply.votes -= 1
    except Vote.DoesNotExist:
        Vote.objects.create(user=request.user, reply=reply)
        reply.votes += 1

    reply.save()
    return redirect('topic_detail', topic_id=reply.topic.id)

@login_required
def delete_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)
    topic_id = reply.topic.id
    if request.user != reply.author:
        return redirect('topic_detail', topic_id=topic_id)
    reply.delete()
    return redirect('topic_detail', topic_id=topic_id)


#----------------------------------------------------------------------------------------
@login_required
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.groups.filter(name="Moderadores").exists()))
def create_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tag_list')  # Substitua com o nome da URL para listar tags
    else:
        form = TagForm()
    return render(request, 'tags/create_tag.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.groups.filter(name="Moderadores").exists()))
def delete_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    if request.method == 'POST':
        tag.delete()
        return redirect('tag_list')
    return render(request, 'tags/confirm_delete.html', {'tag': tag})

def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'tags/tag_list.html', {'tags': tags})

def topics_by_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    topics = tag.topics.all()
    return render(request, 'tags/topics_by_tag.html', {'tag': tag, 'topics': topics})

