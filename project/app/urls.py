from django.urls import path
from . import views

urlpatterns = [
    path("todo/<int:id>", views.todoView, name="todo"),
    path("delete/<int:id>", views.deleteView, name="delete"),
    path("logout", views.logoutView, name="logout"),
    path("login/", views.loginView, name="login"),
    # this debug url should be remove!
    path("debug/", views.debugView, name="debug"),
    path("", views.homeView, name="home")
]
