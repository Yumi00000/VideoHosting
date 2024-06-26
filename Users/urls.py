from django.urls import path
from Users import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.user_cabinet, name="user"),
    path("videos/<username>/", views.user_profile, name="user_profile"),
    path("register/", views.register_handler, name="register_handler"),
    path("login/", views.login_handler, name="login_handler"),
    path("logout/", views.logout_handler, name="logout_handler"),
    path("activate/<user_signed>", views.activate, name="activate"),
    path(
        "password-change/",
        views.change_password,
        name="password_change",
    ),
    path("followers/<int:user_id>/", views.followers_page_view, name="followers_page_view"),
    path("followings/<int:user_id>/", views.following_page_view, name="followers_page_view"),
    path("history/<int:user_id>/", views.history_view, name="history_view"),
]
