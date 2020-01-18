from django.contrib import admin

from pdfurls.models import URL, PDFFile

admin.site.register(PDFFile)
admin.site.register(URL)
