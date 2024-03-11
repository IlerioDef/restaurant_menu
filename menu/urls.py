from django.contrib.auth.views import LogoutView
from django.urls import path

from menu import views
from menu.views import ItemListView, OrderView, ItemDetailView, OrderModifyView, OrderCheckoutView

app_name = 'menu'

urlpatterns = [
    path('', ItemListView.as_view(), name="all"),
    path('item/<int:pk>', ItemDetailView.as_view(), name='item'),
    path('order/', OrderView.as_view(), name='order'),
    path('item/<int:pk>/<str:action>', OrderModifyView.as_view(), name='order_modify'),
    path('order/checkout', OrderCheckoutView.as_view(), name='order_checkout'),

]
