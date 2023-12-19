from django.urls import path
from django.views.generic import TemplateView

from menu import views
from menu.views import ItemListView

app_name = 'menu'

urlpatterns = [
    path('', views.ItemListView.as_view(), name="all"),
    path('item/<int:pk>', views.ItemDetailView.as_view(), name='item'),
]
