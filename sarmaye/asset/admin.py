from django.contrib.admin import register, ModelAdmin
from .models import Asset

@register(Asset)
class AssetAdmin(ModelAdmin):
    list_display = ['name', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
