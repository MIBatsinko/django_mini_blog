from django.contrib import admin
from .models import RatingStar, Rating

admin.site.register(RatingStar)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", "article", 'user')
