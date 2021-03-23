from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('article.urls')),
    path('api/', include('comment.urls')),

    path('', include('blog.urls')),
    path('blog/', include('blog.urls')),
]

urlpatterns += doc_urls
