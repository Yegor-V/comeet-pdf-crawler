import threading

import PyPDF2
import requests

from pdfurls.models import PDFFile


def get_urls_from_pdf_file(pdf_file):
    """
    Gets links from PDF file.

    :param pdf_file: File
        PDF file to get links from
    :return: List
        Links from PDF file
    """
    annots = '/Annots'
    anchor = '/A'
    uri = '/URI'

    reader = PyPDF2.PdfFileReader(pdf_file)

    links = []

    for page in range(reader.numPages):
        page_object = reader.getPage(page).getObject()
        if annots in page_object.keys():
            annotations = page_object[annots]
            for annotation in annotations:
                annotation_object = annotation.getObject()
                if (anchor in annotation_object.keys() and
                    uri in annotation_object[anchor].keys()):
                    links.append(annotation_object[anchor][uri])

    return links


def spawn_urls_check(pdf_file_id):
    """
    Spawns check_urls function in separate thread

    :param pdf_file_id: Int
        PDFFile object database ID
    """
    t = threading.Thread(target=check_urls, args=(pdf_file_id,))
    t.setDaemon(True)
    t.start()


def check_urls(pdf_file_id):
    """
    Checks all URLs found in PDFFile with given ID for if they are alive.

    :param pdf_file_id: Int
         PDFFile object database ID
    """
    pdf_file = PDFFile.objects.get(id=pdf_file_id)
    urls = pdf_file.urls.filter(is_alive__isnull=True)
    for url in urls:
        try:
            res = requests.get(url.link)
        except requests.exceptions.RequestException:
            url.is_alive = False
        else:
            if res.ok:
                url.is_alive = True
            else:
                url.is_alive = False
        url.save()
