from django.contrib import admin
from .models import UserProfile, RatingStar, Rating

admin.site.register(UserProfile)
admin.site.register(RatingStar)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", "article", "ip", 'user')
