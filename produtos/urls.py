from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, ProdutoViewSet, PedidoViewSet, PedidoItemViewSet

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'produtos', ProdutoViewSet)
router.register(r'pedidos', PedidoViewSet)
router.register(r'pedido-itens', PedidoItemViewSet)

urlpatterns = router.urls
