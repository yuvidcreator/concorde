from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from investCore.settings import DEBUG

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('concorde.urls')),
]


urlpatterns +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = 'Investment'
admin.site.index_title = 'Investment'
admin.site.site_title = 'Investment Admin Panel'