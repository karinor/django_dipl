from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static, settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('', include('Pages.urls', namespace='pages')),
    path('catalog/', include('catalog.urls', namespace='catalog')),
    path('profile/', include('account.urls', namespace='account')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
