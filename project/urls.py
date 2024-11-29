from django.urls import path 

from .views import ProductListView, CouponPriceView, ProductDetailView

urlpatterns = [
    path(
        "get-product-list",
        ProductListView.as_view(),
        name="get-product-list",
    ),
        path(
        "get-product-detail",
        ProductDetailView.as_view(),
        name="get-product-detail",
    ),
     path(
        "get-coupon-price",
        CouponPriceView.as_view(),
        name="get-coupon-price",
    ),
]