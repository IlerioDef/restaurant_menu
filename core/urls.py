from django.contrib.auth import admin
from django.urls import path

app_name = 'core'

urlpatterns = [
    path('admin/', admin.site.urls),  # Keep

]



