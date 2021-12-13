from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers
from machines.views import RawDataViewSet
from .view import main_index, register, edit, validate, not_validate, validate_phone

urlpatterns = [
                  url(r'^$', main_index),
                  url(r'^machines/', include('machines.urls')),
                  url(r'^admin/', admin.site.urls),
                  url(r'^accounts/', include('django.contrib.auth.urls')),
                  url(r'^accounts/register/$', register, name='register'),
                  url(r'^accounts/edit/$', edit, name='edit'),
                  url(r'^accounts/validate/$', validate, name='validate'),
                  url(r'^accounts/not_validate/$', not_validate, name='not_validate'),
                  url(r'^validate_phone/$', validate_phone, name='validate_phone'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)