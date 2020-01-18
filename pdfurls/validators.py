import PyPDF2
from PyPDF2.utils import PdfReadError
from rest_framework import serializers


def validate_file(value):
    try:
        PyPDF2.PdfFileReader(value)
    except PdfReadError:
        raise serializers.ValidationError('Can not open PDF file')
