from tempfile import NamedTemporaryFile

from django.test import TestCase
from rest_framework.test import APIClient

from pdfurls.models import URL, PDFFile


class TestApi(TestCase):
    maxDiff = None

    def setUp(self):
        self.pdf_file_1 = PDFFile.objects.create(name='test_1.pdf')
        self.pdf_file_2 = PDFFile.objects.create(name='test_2.pdf')

        self.url_1 = URL.objects.create(link='https://example.com/path/1/')
        self.url_2 = URL.objects.create(link='https://example.com/path/2/')
        self.url_3 = URL.objects.create(link='https://example.com/path/3/')
        self.url_4 = URL.objects.create(link='https://example.com/path/4/')

        self.pdf_file_1.urls.add(self.url_1, self.url_2, self.url_3)
        self.pdf_file_2.urls.add(self.url_4)

        self.file = NamedTemporaryFile()
        self.file.write('Some data')
        self.file.close()

        self.client = APIClient()

    def test_pdf_files_list_get(self):
        res = self.client.get('/api/v1/pdf_files/')
        self.assertEquals(res.status_code, 200)
        self.assertEquals(
            res.json(),
            [
                {
                    'id': self.pdf_file_1.id,
                    'name': 'test_1.pdf',
                    'links_number': 3
                },
                {
                    'id': self.pdf_file_2.id,
                    'name': 'test_2.pdf',
                    'links_number': 1
                }
            ]
        )

    def test_pdf_files_detail_get(self):
        res = self.client.get(
            '/api/v1/pdf_files/{}/'.format(self.pdf_file_1.id))
        self.assertEquals(res.status_code, 200)
        self.assertEquals(
            res.json(),
            {
                'id': self.pdf_file_1.id,
                'name': 'test_1.pdf',
                'links_number': 3
            }
        )

    def test_urls_list_get(self):
        res = self.client.get('/api/v1/urls/')
        self.assertEquals(res.status_code, 200)
        self.assertEquals(
            res.json(),
            [
                {
                    'id': self.url_1.id,
                    'link': 'https://example.com/path/1/',
                    'is_alive': None,
                    'pdf_files_number': 1
                },
                {
                    'id': self.url_2.id,
                    'link': 'https://example.com/path/2/',
                    'is_alive': None,
                    'pdf_files_number': 1
                },
                {
                    'id': self.url_3.id,
                    'link': 'https://example.com/path/3/',
                    'is_alive': None,
                    'pdf_files_number': 1
                },
                {
                    'id': self.url_4.id,
                    'link': 'https://example.com/path/4/',
                    'is_alive': None,
                    'pdf_files_number': 1
                }
            ]
        )

    def test_urls_detail_get(self):
        res = self.client.get('/api/v1/urls/{}/'.format(self.url_1.id))
        self.assertEquals(res.status_code, 200)
        self.assertEquals(
            res.json(),
            {
                'id': self.url_1.id,
                'link': 'https://example.com/path/1/',
                'is_alive': None,
                'pdf_files_number': 1
            }
        )

    def test_pdf_file_urls_list_get(self):
        res = self.client.get(
            '/api/v1/pdf_files/{}/urls/'.format(self.pdf_file_2.id))
        self.assertEquals(res.status_code, 200)
        self.assertEquals(
            res.json(),
            [
                {
                    'id': self.url_4.id,
                    'link': 'https://example.com/path/4/',
                    'is_alive': None,
                    'pdf_files_number': 1
                }
            ]
        )
