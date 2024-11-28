from django.urls import path 

from .views import TestView, TestProductView, CouponPriceView


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
     path(
        "test3",
        CouponPriceView.as_view(),
        name="test3",
    ),
]