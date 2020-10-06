"""BlueBlogOverhauled URL Configuration

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
from blog import views
from django.contrib.auth import views as authentication_views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "BlueBlog Administration"
admin.site.site_title = "BlueBlog Admin Panel"
admin.site.index_title = "Welcome to BlueBlog Admin Panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('blog.urls')),
    path('register/', include('register.urls')),
    path('blog/', include(('blog.urls', 'blog'), namespace='posts')),

    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/',
         authentication_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),

    path('password_change/',
         authentication_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
         name='password_change'),

    path('password_reset/done/',
         authentication_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', authentication_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

    path('password_reset/', authentication_views.PasswordResetView.as_view(), name='password_reset'),


    path('reset/done/',
         authentication_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete'
                                                                              '.html'),
         name='password_reset_complete'),
]
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
