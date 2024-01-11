from django.urls import path, include
from django.views.generic import TemplateView

from menu.views import order

app_name = 'core'

urlpatterns = [
    path("", TemplateView.as_view(template_name='core/base.html'), name="index"),
]



