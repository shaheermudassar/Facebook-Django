from django.urls import path, include
from userauths import views

app_name = 'userauths'

urlpatterns = [
    path("signup", views.register_views, name="signup"),
    path("signin", views.login_view, name="signin"),
    path("signout", views.logout_view, name="signout"),
]


