from django.urls import path
from django.views.generic import TemplateView

from menu import views
from menu.views import ItemView

app_name = 'menu'

urlpatterns = [
    path('', views.ItemView.as_view(), name="all"),
    # path('/<int:menu_id>/', views.menu, name='item'),
]
