from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers

from pdfurls import views

router = routers.SimpleRouter()
router.register(r'pdf_files', views.PDFFileViewSet)
router.register(r'urls', views.URLViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include(router.urls))
]
