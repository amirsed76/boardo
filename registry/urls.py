from django.urls import path, include, re_path

import rest_auth.urls

from . import views
import rest_auth.urls
import rest_auth.registration.urls

urlpatterns = \
    [
        # path('password-reset-confirm/', views.PasswordResetConfirmView.as_view(),
        #      name="password_reset_confirm"),
        # path('password-reset-confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(),
        #      name="password_reset_confirm"),
        # path('recovery/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(),
        #      name="password_reset_confirm"),
        path("avatars/",views.AvatarListApiView.as_view()),
        path('', include('rest_auth.urls')),
        path('registration/', include('rest_auth.registration.urls')),

    ]
