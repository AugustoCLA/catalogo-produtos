from django.contrib import admin
from .models import Categoria, Produto, Pedido, PedidoItem


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'descricao']
    search_fields = ['nome']


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'preco', 'estoque', 'categoria']
    list_filter = ['categoria']
    search_fields = ['nome']
    list_select_related = ['categoria']


class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 0
    fields = ['produto', 'quantidade', 'preco_unitario']


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'total', 'criado_em']
    list_filter = ['status']
    inlines = [PedidoItemInline]


@admin.register(PedidoItem)
class PedidoItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'pedido', 'produto', 'quantidade', 'preco_unitario']
    list_filter = ['pedido__status']
    search_fields = ['produto__nome']
