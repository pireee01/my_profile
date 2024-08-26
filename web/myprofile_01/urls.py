"""
URL configuration for myprofile_01 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('microblogging/', views.microblogging, name='microblogging'),
    path('microblog/<int:pk>/', views.microblog_detail, name='microblog_detail'),
    path('microblog/', views.microblog_list, name='microblog_list'),
    path('certificates/', views.certificates, name='certificates'),
    path('certificates/<int:pk>/', views.certificate_detail, name='certificate_detail'),
    path('certificates/new/', views.certificate_new, name='certificate_new'),
    path('certificates/<int:pk>/edit/', views.certificate_edit, name='certificate_edit'),
    path('certificates/<int:pk>/delete/', views.certificate_delete, name='certificate_delete'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('chat/', views.chat, name='chat'),  # Add this line for the chat API
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
