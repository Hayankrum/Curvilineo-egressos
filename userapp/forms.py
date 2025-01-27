from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class EditProfileForm(forms.ModelForm):
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        required=False,
        label="Biografia"
    )
    profile_picture = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        required=False,
        label="Foto de Perfil"
    )
    remove_profile_picture = forms.BooleanField(
        required=False,
        label="Remover Foto de Perfil"
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user_profile = kwargs.pop('user_profile', None)
        super().__init__(*args, **kwargs)
        if user_profile:
            self.fields['bio'].initial = user_profile.bio
            self.fields['profile_picture'].initial = user_profile.profile_picture

    def save(self, commit=True, user_profile=None):
        user = super().save(commit=False)
        if commit:
            user.save()
            if user_profile:
                user_profile.bio = self.cleaned_data.get('bio', user_profile.bio)
                
                # Se o campo de remover foto estiver marcado, remove a foto de perfil
                if self.cleaned_data.get('remove_profile_picture') and user_profile.profile_picture:
                    # Exclui a foto do perfil atual
                    user_profile.profile_picture.delete(save=False)  
                    user_profile.profile_picture = None  # Remove a foto de perfil do modelo

                # Se não for para remover, verifica se há uma nova foto para salvar
                if not self.cleaned_data.get('remove_profile_picture'):
                    profile_picture = self.cleaned_data.get('profile_picture')
                    if profile_picture:
                        user_profile.profile_picture = profile_picture
                        
                user_profile.save()
        return user
