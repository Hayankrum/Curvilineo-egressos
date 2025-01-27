from django.urls import path
from . import views

urlpatterns = [
    # URLs para Classe
    path('classe/', views.classe_list, name='classe_list'),
    path('classe/create/', views.create_classe, name='create_classe'),
    path('classe/edit/<int:classe_id>/', views.edit_classe, name='edit_classe'),
    path('classe/delete/<int:classe_id>/', views.delete_classe, name='delete_classe'),

    # URLs para SubCategoria
    path('classe/<int:classe_id>/subcategoria/', views.subcategoria_list, name='subcategoria_list'),
    path('classe/<int:classe_id>/subcategoria/create/', views.create_subcategoria, name='create_subcategoria'),
    path('subcategoria/edit/<int:subcategoria_id>/', views.edit_subcategoria, name='edit_subcategoria'),
    path('subcategoria/delete/<int:subcategoria_id>/', views.delete_subcategoria, name='delete_subcategoria'),

    # URLs para Topic
    path('subcategoria/<int:subcategoria_id>/topic/', views.topic_list, name='topic_list'),
    path('topic/<int:topic_id>/', views.topic_detail, name='topic_detail'),
    path('subcategoria/<int:subcategoria_id>/topic/create/', views.create_topic, name='create_topic'),
    path('topic/edit/<int:topic_id>/', views.edit_topic, name='edit_topic'),
    path('topic/delete/<int:topic_id>/', views.delete_topic, name='delete_topic'),

    # URLs para Reply
    path('topic/<int:topic_id>/reply/add/', views.add_reply, name='add_reply'),
    path('reply/edit/<int:reply_id>/', views.edit_reply, name='edit_reply'),
    path('reply/vote/<int:reply_id>/', views.vote_reply, name='vote_reply'),
    path('reply/delete/<int:reply_id>/', views.delete_reply, name='delete_reply'),

    path('tags/', views.tag_list, name='tag_list'),
    path('tags/create/', views.create_tag, name='create_tag'),
    path('tags/<int:tag_id>/delete/', views.delete_tag, name='delete_tag'),
    path('tags/<int:tag_id>/topics/', views.topics_by_tag, name='topics_by_tag')
]
