"CORE URL FILE (Note: We can have multiple)"
"We are going to have two URL files here. One root and one for our specific application"

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include ('base.urls')),
    path('api/', include('base.api.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )
