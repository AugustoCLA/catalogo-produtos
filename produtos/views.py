from rest_framework import viewsets
from .models import Categoria, Produto, Pedido, PedidoItem
from .serializers import CategoriaSerializer, ProdutoSerializer, PedidoSerializer, PedidoItemSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.prefetch_related('itens__produto').all()
    serializer_class = PedidoSerializer


class PedidoItemViewSet(viewsets.ModelViewSet):
    queryset = PedidoItem.objects.select_related('pedido', 'produto').all()
    serializer_class = PedidoItemSerializer
