from rest_framework.routers import DefaultRouter
from shop.orders.views import OrderViewSet, OrderItemViewSet

router = DefaultRouter()

router.register(r'orders', OrderViewSet)
router.register(r'order_items', OrderItemViewSet)


urlpatterns = router.urls