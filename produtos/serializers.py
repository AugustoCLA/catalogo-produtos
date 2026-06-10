from rest_framework import serializers
from .models import Categoria, Produto, Pedido, PedidoItem


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'descricao']


class ProdutoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)

    class Meta:
        model = Produto
        fields = ['id', 'nome', 'descricao', 'preco', 'estoque', 'imagem', 'categoria', 'categoria_nome']


class PedidoItemSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = PedidoItem
        fields = ['id', 'pedido', 'produto', 'produto_nome', 'quantidade', 'preco_unitario', 'subtotal']


class PedidoSerializer(serializers.ModelSerializer):
    itens = PedidoItemSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = ['id', 'status', 'criado_em', 'atualizado_em', 'total', 'itens']
