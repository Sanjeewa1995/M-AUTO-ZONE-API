from django.urls import path, include
from rest_framework.routers import DefaultRouter
from store.views import ProductViewSet, CartViewSet, CartItemViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'cart-items', CartItemViewSet, basename='cart-item')

urlpatterns = [
    path('', include(router.urls)),
]
