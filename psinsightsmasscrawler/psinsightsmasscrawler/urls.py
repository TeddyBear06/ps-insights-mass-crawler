from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('crawler/', include('crawler.urls')),
    path('admin/', admin.site.urls),
]