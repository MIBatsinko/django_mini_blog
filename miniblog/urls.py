from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as doc_urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('articles/', include([
            path('', include('article.urls')),
            path('categories/', include('article.urls')),
        ])),
        # path('comments/', include('comment.urls')),
        path('users/', include('users.urls')),
        # path('articles/', include('article.urls')),
        path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    ])),

    path('', include('blog.urls')),
    path('comments/', include('comment.urls')),
    path('payments/', include('payments.urls')),
    path('my_account/', include('my_account.urls')),
    path('accounts/', include('allauth.urls')),
    path('admin_panel/', include('admin_panel.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += doc_urls
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
