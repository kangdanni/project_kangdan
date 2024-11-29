from django.urls import path 

from .views import ProductListView, CouponPriceView, ProductDetailView

urlpatterns = [
    path(
        "test",
        ProductListView.as_view(),
        name="test",
    ),
        path(
        "test2",
        ProductDetailView.as_view(),
        name="test2",
    ),
     path(
        "test3",
        CouponPriceView.as_view(),
        name="test3",
    ),
]