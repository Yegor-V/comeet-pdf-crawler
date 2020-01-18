from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from pdfurls.models import URL, PDFFile
from pdfurls.serializers import PDFFileSerializer, URLSerializer


class PDFFileViewSet(viewsets.ModelViewSet):
    queryset = PDFFile.objects.annotate(
        links_number=Count('urls')).order_by('id')
    serializer_class = PDFFileSerializer
    http_method_names = ['get', 'post', 'head', 'options']

    @action(methods=['get'], detail=True)
    def urls(self, request, pk=None):
        """
        Returns all links found in PDF file.
        """
        pdf_file = self.get_object()
        urls = URLViewSet.queryset.filter(pdf_files=pdf_file)
        serializer = URLSerializer(urls, many=True)
        return Response(serializer.data)


class URLViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = URL.objects.annotate(
        pdf_files_number=Count('pdf_files')).order_by('id')
    serializer_class = URLSerializer
