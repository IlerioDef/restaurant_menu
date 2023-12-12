from django.urls import path
from django.views.generic import TemplateView

from menu import views

app_name = 'menu'

urlpatterns = [
    # path('', TemplateView.as_view(template_name=''), name="all"),
    # path('/<int:menu_id>/', views.menu, name='item'),
]
