from django.urls import path 

from .views import TestView, TestProductView


urlpatterns = [
    path(
        "test",
        TestView.as_view(),
        name="test",
    ),
        path(
        "test2",
        TestProductView.as_view(),
        name="test2",
    ),
]