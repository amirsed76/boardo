from django.urls import path

from . import views

urlpatterns = [
    # path('<str:room_name>/', views.room, name='room'),
    path("create_server", views.CatanEventCreateApiView.as_view()),
    path("server/<str:room_name>", views.LoginGameAPIView.as_view()),
    path("map/<str:room_name>", views.TileListAPIVIew.as_view()),
    path("player_info/<str:room_name>", views.PlayerInformationListAPIView.as_view()),
    path("personal/<str:room_name>", views.PersonalInformation.as_view()),
    path("init1/<str:room_name>", views.Init1APIView.as_view()),
    path("init2/<str:room_name>", views.Init2APIView.as_view()),
    path("play_year_of_plenty/<str:room_name>", views.PlayYearOfPlenty.as_view()),
    path("play_road_building/<str:room_name>", views.PlayRoadBuilding.as_view()),
    path("play_monopoly/<str:room_name>", views.PlayMonopoly.as_view()),
    path("dice/<str:room_name>", views.DiceAPIView.as_view()),

    path("create_home/<str:room_name>", views.HomeCreateAPIView.as_view()),
    path("create_city/<str:room_name>/<int:pk>", views.CityUpdateAPIView.as_view()),
    path("create_road/<str:room_name>", views.RoadCreateAPIView.as_view()),
    path("trade/<str:room_name>", views.TradAPIView.as_view()),
    path("trade_bank/<str:room_name>", views.BankTrade.as_view()),

    path("end/<str:room_name>", views.EndRound.as_view()),
    # TODO buy development card
    # TODO trad
]
