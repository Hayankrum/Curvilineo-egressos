from django import template

register = template.Library()

@register.filter
def can_create(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name="Moderadores").exists())
