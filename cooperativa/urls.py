from django.contrib import admin
from django.urls import path, include

from django.conf import settings               # ADICIONADO
from django.conf.urls.static import static     # ADICIONADO

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reciclagem.urls')),
]

# ADICIONADO - Para servir arquivos de mídia (fotos, etc.) em ambiente de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
