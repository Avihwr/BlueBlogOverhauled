"""BlueBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from blog import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('search/', views.search, name='search'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('posts/<str:slug>', views.posts, name='posts'),
    path('profile/', views.profile_edit, name='profile_edit'),
    path('post_upload/', views.post_upload, name='post_upload'),
    path('post_edit/<pk>', views.post_edit, name='post_edit'),
    path('post_list', views.posts_list, name='post_list'),
    path('post_delete/<str:slug>', views.post_delete, name='post_delete'),
    path('comment_delete/<int:sno>', views.comment_delete, name='comment_delete'),
    path('reply_delete/<int:sno>/<int:parent_id>', views.reply_delete, name='reply_delete'),
    path('excerpt/', views.excerpt, name='excerpt'),
    path('tag/<str:slug>', views.tagged, name='tagged'),
    path('category/<str:category>', views.Category, name='category'),
    path('posts/', views.posts_redirect, name='posts_redirect'),
    path('post_edit/', views.posts_edit_redirect, name='posts_edit_redirect'),

]
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
