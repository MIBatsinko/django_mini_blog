from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.AdminHome.as_view(), name='admin_index'),
    path('users/', include([
        path('', views.AdminUsersView.as_view(), name='users'),
        path('user_info/<int:pk>/', views.AdminUserProfileView.as_view(), name='user_info'),
        path('edit/<int:pk>/', views.AdminUserProfileUpdateView.as_view(), name='user_edit'),
        path('deactivate/<int:pk>/', views.AdminUserIsActive.deactivate, name='deactivate'),
        path('activate/<int:pk>/', views.AdminUserIsActive.activate, name='activate'),
    ])),

    path('articles/', include([
        path('', views.AdminArticlesView.as_view(), name='articles'),
        path('add/', views.AdminArticleCreateView.as_view(), name='article_add'),
        path('details/<int:pk>/', views.AdminArticleDetailView.as_view(), name='article_details'),
        path('edit/<int:pk>/', views.AdminArticleUpdateView.as_view(), name='article_edit'),
        path('delete/<int:pk>/', views.AdminArticleDeleteView.as_view(), name='article_delete'),
        path('comment/', include([
            path('<int:pk>/edit', views.AdminCommentUpdateView.as_view(), name='admin_comment_edit'),
            path('<int:pk>/delete', views.AdminCommentDeleteView.as_view(), name='admin_comment_delete'),
            path('<int:article_id>/comment_add/', views.AdminCommentCreateView.as_view(), name='admin_comment_add'),
        ]))
    ])),

    path('categories/', include([
        path('', views.AdminCategoriesView.as_view(), name='categories'),
        path('add/', views.AdminCategoryCreateView.as_view(), name='category_add'),
        path('edit/<int:pk>/', views.AdminCategoryUpdateView.as_view(), name='category_edit'),
        path('delete/<int:pk>/', views.AdminCategoryDeleteView.as_view(), name='category_delete'),
    ])),

]
