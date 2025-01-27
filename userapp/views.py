from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from userapp.models import UserProfile
from base.models import Classe, SubCategoria, Topic, Reply, Vote, Tag
#---------------------------------------------------------------------------

def home(request):
    return render(request, 'home.html')

# Função de login (manteve a lógica que você já tinha)
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('userapp:home')  # Substitua 'cessao1' pelo nome correto da sua página
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'login.html')

# Função de logout
def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu com sucesso.')
    return redirect('userapp:login')

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

def assign_permissions_to_group(group):
    # Exemplo: Atribuir permissões de leitura a um modelo específico
    content_type = ContentType.objects.get_for_model(User)
    permissions = Permission.objects.filter(content_type=content_type)

    for perm in permissions:
        group.permissions.add(perm)

def register_view(request):
    if request.method == 'POST':
        try:
            # Captura os dados do formulário
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            grupo_id = request.POST['grupo']

            # Validação das senhas
            if password1 != password2:
                messages.error(request, 'As senhas não coincidem.')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Nome de usuário já está em uso.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'E-mail já está cadastrado.')
            else:
                # Criação do usuário
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()

                # Associando o usuário ao grupo escolhido
                grupo = Group.objects.get(id=grupo_id)
                user.groups.add(grupo)

                # Chama a função para atribuir permissões automaticamente ao grupo
                assign_permissions_to_group(grupo)

                # Criar ou atualizar o perfil do usuário com os dados adicionais
                profile = UserProfile(
                    user=user,
                    group=grupo,
                )
                profile.save()

                # Mensagem de sucesso e redirecionamento
                messages.success(request, 'Conta criada com sucesso! Faça login.')
                return redirect('userapp:login')

        except KeyError as e:
            messages.error(request, f'O campo {e} não foi enviado corretamente.')
        except Group.DoesNotExist:
            messages.error(request, 'Grupo selecionado inválido.')
        except Exception as e:
            messages.error(request, f'Ocorreu um erro: {e}')
    
    # Passa os grupos para o template para permitir a escolha
    grupos = Group.objects.all()
    return render(request, 'register.html', {'grupos': grupos})




# Função para redefinir senha
def password_reset_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Redefinição de senha"
                    email_template_name = "password_reset_email.html"
                    context = {
                        "email": user.email,
                        "domain": request.get_host(),
                        "site_name": "Seu Site",
                        "uid": user.id,
                        "token": "gerar_token",  # Substituir por uma lógica para token real
                    }
                    email_content = render_to_string(email_template_name, context)
                    send_mail(subject, email_content, settings.DEFAULT_FROM_EMAIL, [user.email])
                messages.success(request, 'E-mail de redefinição de senha enviado.')
                return redirect('userapp:login')
            else:
                messages.error(request, 'Nenhum usuário encontrado com este e-mail.')
    return render(request, 'password_reset.html')



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages


def profile_view(request):
    return render(request, 'profile.html')



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EditProfileForm

@login_required
def edit_profile(request):
    user_profile = request.user.userprofile  # Supondo que você tenha um modelo relacionado
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, user_profile=user_profile, instance=request.user)
        if form.is_valid():
            form.save(user_profile=user_profile)  # Passando user_profile para salvar os dados corretamente
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('userapp:profile')
    else:
        form = EditProfileForm(user_profile=user_profile, instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})

@login_required
def delete_account(request):
    if request.method == "POST":
        password = request.POST.get('password')
        delete_actions = request.POST.get('delete_actions')  # 'yes' ou 'no'

        user = request.user

        # Verificar se a senha fornecida está correta
        if not authenticate(username=user.username, password=password):
            messages.error(request, "Senha incorreta. Tente novamente.")
            return redirect('delete_account')

        # Se o usuário escolheu excluir as ações
        if delete_actions == 'yes':
            # Excluir tópicos criados pelo usuário
            user.topic_set.all().delete()

            # Excluir respostas criadas pelo usuário
            Reply.objects.filter(author=user).delete()

            # Excluir votos do usuário
            Vote.objects.filter(user=user).delete()
            """
            # Excluir classes e subcategorias associadas
            for classe in user.classes.all():
                classe.subcategorias.all().delete()
                classe.delete()
            """
        # Excluir a conta do usuário
        user.delete()
        messages.success(request, "Sua conta foi excluída com sucesso!")
        return redirect('userapp:login')  # Redireciona para a página de login

    return render(request, 'delete_account.html')





