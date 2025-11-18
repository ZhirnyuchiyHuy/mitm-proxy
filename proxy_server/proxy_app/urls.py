from django.urls import path
from . import views

app_name = 'proxy_app'

urlpatterns = [
    path('', views.index, name='index'),
    path("add/", views.add_network, name="add"),
    path("edit/<int:pk>/", views.edit_network, name="edit"),
    path("delete/<int:pk>/", views.delete_network, name="delete"),
    path("toggle/<int:pk>/", views.toggle_network, name="toggle"),
]

