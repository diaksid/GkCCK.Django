from django.contrib import admin

from .image import ImageModelAdmin, ImageTabularInlineAdmin, ImageGenericTabularInlineAdmin, ImageStackedInlineAdmin, ImageGenericStackedInlineAdmin
from .albom import AlbomModelAdmin, AlbomTabularInlineAdmin, AlbomGenericTabularInlineAdmin, AlbomStackedInlineAdmin, AlbomGenericStackedInlineAdmin

from ..models import Image, Albom


__all__ = [
    'ImageModelAdmin', 'ImageTabularInlineAdmin', 'ImageGenericTabularInlineAdmin', 'ImageStackedInlineAdmin', 'ImageGenericStackedInlineAdmin',
    'AlbomModelAdmin', 'AlbomTabularInlineAdmin', 'AlbomGenericTabularInlineAdmin', 'AlbomStackedInlineAdmin', 'AlbomGenericStackedInlineAdmin',
]

admin.site.register(Image, ImageModelAdmin)

admin.site.register(Albom, AlbomModelAdmin)
