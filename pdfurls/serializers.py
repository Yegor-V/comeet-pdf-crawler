from rest_framework import serializers

from pdfurls.models import URL, PDFFile
from pdfurls.validators import validate_file


class PDFFileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True, validators=[validate_file])
    links_number = serializers.IntegerField(read_only=True)

    class Meta:
        model = PDFFile
        fields = ['id', 'name', 'file', 'links_number']
        read_only_fields = ('id', 'name', 'links_number')

    def create(self, validated_data):
        return PDFFile.objects.create_from_file(validated_data['file'])


class URLSerializer(serializers.ModelSerializer):
    pdf_files_number = serializers.IntegerField(read_only=True)

    class Meta:
        model = URL
        fields = ['id', 'link', 'is_alive', 'pdf_files_number']
