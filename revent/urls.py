from django.contrib import admin
from django.urls import include, path

from photo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.hello, name='hello')
    # In case we wanna have multiple url files for each app
    # path('photo/', include('photo.urls'))
]
