from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from . import views

urlpatterns = \
    [
        path('games/', views.GameListAPIVies.as_view()),
        path('games/<int:pk>', views.GameRetrieveAPIView.as_view()),
        # path('chat/', include('chat.urls')),

    ]