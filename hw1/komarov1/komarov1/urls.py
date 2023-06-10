"""
URL configuration for komarov1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from askme import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'askme'

urlpatterns = [
    path('', views.index, name="index"),
    path('admin/', admin.site.urls),

    path('question/<int:question_id>/', views.question, name="question"),
    path('question/<int:question_id>/page/<int:page_num>', views.question, name='question_page'),

    path('hot/', views.hot, name="hot"),
    path('tag/<name_tag>/', views.tag, name="tag"),
    path('login/', views.log_in, name="login"),
    path('logout/', views.log_out, name="logout"),
    path('register/', views.register, name="register"),
    path('ask/', views.ask, name="ask"),
    path('settings/', views.settings, name="settings"),
    path('vote_up/', views.vote_up, name='vote_up')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
