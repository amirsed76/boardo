from django.urls import path

from . import views

urlpatterns = [
    path('<str:room_name>/', views.room, name='room'),
    path("create_server", views.CatanEventCreateApiView.as_view()),
    path("server/<str:room_name>", views.LoginGameAPIView.as_view()),
    path("personal/<str:room_name>", views.PersonalInformation.as_view()),
    path("map/<str:room_name>", views.TileListAPIVIew.as_view()),
    path("player_info/<str:room_name>", views.PlayerInformationListAPIView.as_view()),
    path("init1/<str:room_name>", views.Init1APIView.as_view()),
    path("init2/<str:room_name>", views.Init2APIView.as_view()),
    path("play_year_of_plenty/<str:room_name>",views.PlayYearOfPlenty.as_view()),
    path("create_home/<str:room_name>", views.HomeCreateAPIView.as_view()),
    path("create_city/<int:id>", views.CityUpdateAPIView.as_view()),
    # TODO create road
    # TODO buy development card
    # TODO play monopoly card
    # TODO play road_building_card
    # TODO play year_of_plenty card
    # TODO knight_card
    # TODO trad
]
