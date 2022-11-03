from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('products/<int:category_id>/', views.products, name='category'),
    path('products/<int:page>', views.products, name='page'),
    path('basket-add/<int:product_id>', views.basket_add, name="basket_add"),
    path('products/basket-delete/<int:id>', views.basket_delete, name="basket_delete"),
    path('post/<slug:product_slug>/', views.DetailProduct.as_view(), name='product'),
]

