from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('Accounts.urls')),
    path('', include('WebScraper.urls')),
    path('ai/', include('WebScraper.urls')),
]
