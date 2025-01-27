from django.contrib import admin
from .models import Classe, SubCategoria, Topic, Reply, Vote, Tag

admin.site.register(Classe)
admin.site.register(SubCategoria)
admin.site.register(Topic)
admin.site.register(Reply)
admin.site.register(Vote)
admin.site.register(Tag)

class ClasseAdmin(admin.ModelAdmin):
    list_display = ('name', 'publico')
    filter_horizontal = ('grupos_permitidos', 'usuarios_permitidos')