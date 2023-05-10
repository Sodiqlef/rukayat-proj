"""notesharing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from notes import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from notesharing import settings as st

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='notes/login.html', next_page = st.LOGIN_REDIRECT_URL), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page = st.LOGOUT_REDIRECT_URL), name='logout'),
    path('', views.note_list, name='note_list'),
    path('note/new/', views.note_new, name='note_new'),
    path('note/<int:pk>/delete/', views.note_delete, name='note_delete'),
    re_path(r'^note/(?P<pk>[0-9]+)/edit/$', views.note_edit, name='note_edit'),
    re_path(r'^note/(?P<pk>\d+)/share/$', views.note_share, name='note_share'),
    re_path(r'^note/(?P<pk>\d+)/$', views.note_detail, name='note_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)