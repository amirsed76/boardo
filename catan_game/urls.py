from django.urls import path

from . import views

urlpatterns = [
    path('<str:room_name>/', views.room, name='room'),
    path("create_server", views.CatanEventCreateApiView.as_view()),
    path("server/<str:room_name>", views.PlayerGameCreateApiView.as_view()),
    path("personal/<str:room_name>", views.PersonalInformation.as_view()),
    path("map/<str:room_name>", views.TileListAPIVIew.as_view()),
    path("player_info/<str:room_name>", views.PlayerInformationListAPIView.as_view()),
    path("create_home/<str:room_name>", views.HomeCreateAPIView.as_view()),
    path("create_city/<int:id>", views.CityUpdateAPIView.as_view())
]


