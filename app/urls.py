from django.urls import path, include
from . import views
# from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(prefix='products', viewset=views.ProductViewSet)
router.register(prefix='collections', viewset=views.CollectionViewSet)
router.register(prefix='carts', viewset=views.CartViewSet)
router.register(prefix='customers', viewset=views.CustomerViewSet)
router.register(prefix='orders', viewset=views.OrderViewSet)

products_router = routers.NestedDefaultRouter(
    router, parent_prefix='products', lookup='products')
products_router.register(
    'reviews', viewset=views.ReviewViewSet, basename='products-reviews')

carts_router = routers.NestedDefaultRouter(
    router, parent_prefix='carts', lookup='cart')
carts_router.register(
    'items', viewset=views.CartItemViewSet, basename='cart-items')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
    path('', include(carts_router.urls))
]
"""
If a request is made to the products endpoint, it should be handled by products_list view
"""
