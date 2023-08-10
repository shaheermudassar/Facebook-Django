from django.urls import path, include
from messenger import views

app_name = 'messenger'

urlpatterns = [
    path("", views.messenger, name="messenger"),
    path("chat/<id>", views.chat, name="chat"),
    path("search", views.search, name="search")
]