from django.urls import path, include
from django.views.generic import TemplateView

from menu import views
from menu.views import ItemListView

app_name = 'menu'

urlpatterns = [
    path('', views.ItemListView.as_view(), name="all"),
    path('item/<int:pk>', views.ItemDetailView.as_view(), name='item'),
    path('order/', views.order, name='order'),
    path('order/add/', views.order_add, name="order_add"),
    path('order/update/', views.order_update, name="order_update"),
    path('order/delete/', views.order_delete, name="order_delete"),

]
