from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("friends/", views.FriendsView.as_view(), name="friends"),
    path("settings/", views.settings, name="settings"),
    path("talk_room/<user_id>", views.talk_room, name="talk_room"),
    path("username_change/", views.username_change, name="username_change"),
    path(
        "username_change_done/", views.username_change_done, name="username_change_done"
    ),
    path("email_change/", views.email_change, name="email_change"),
    path("email_change_done/", views.email_change_done, name="email_change_done"),
    path(
        "password_change/",
        views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password_change_done/",
        views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]
