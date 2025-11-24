from django.urls import path
from . import views

urlpatterns = [
    path("play/", views.play, name="play"),
    path("step/", views.step, name="step"),
    path("rules/", views.rules, name="rules"),
    path("history/", views.history, name="history"),
]
