from django import forms
from .models import Classe, SubCategoria, Topic, Reply, Tag
from django.contrib.auth.models import User, Group

class ClasseForm(forms.ModelForm):
    class Meta:
        model = Classe
        fields = ['name', 'description', 'grupos_permitidos', 'usuarios_permitidos', 'publico']

    # Adicionando campos para selecionar usuários ou grupos
    grupos_permitidos = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(), 
        required=False,
        widget=forms.CheckboxSelectMultiple(), 
        label="Grupos Permitidos"
    )
    usuarios_permitidos = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(), 
        label="Usuários Permitidos"
    )
    publico = forms.BooleanField(
        required=False,
        initial=True,
        label="Público",
        help_text="Marque para permitir que qualquer usuário tenha acesso à classe."
    )


# Formulário para SubCategoria
class SubCategoriaForm(forms.ModelForm):
    class Meta:
        model = SubCategoria
        fields = ['name', 'description']


class TopicForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Tags"
    )

    class Meta:
        model = Topic
        fields = ['title', 'content', 'tags']


# Formulário para Reply
class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']