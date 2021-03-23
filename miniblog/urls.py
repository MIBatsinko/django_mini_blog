from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('article.urls')),
    path('api/', include('comment.urls')),
]

urlpatterns += doc_urls
