from django.db import models


class PDFFileManager(models.Manager):
    @staticmethod
    def create_from_file(pdf_file):
        """
        Saves PFFile object to db.
        Extracts and saves links from given PDF file.

        :param pdf_file: File
            PDF file to save to db and to extract and save links from
        :return: PDFFile
            ORM PDFFile object
        """
        from pdfurls.utils import get_urls_from_pdf_file, spawn_urls_check

        links = get_urls_from_pdf_file(pdf_file)
        pdf_file, _ = PDFFile.objects.get_or_create(name=pdf_file.name)

        existing_links = URL.objects.filter(link__in=links).values_list(
            'link', flat=True)
        new_links = set(links) - set(existing_links)
        new_urls = [URL(link=link) for link in new_links]

        # Other option is to use SQL UPSERT
        URL.objects.bulk_create(new_urls)
        pdf_file.urls.add(*new_urls)

        spawn_urls_check(pdf_file.id)
        return pdf_file


class PDFFile(models.Model):
    name = models.CharField(max_length=200, unique=True)
    urls = models.ManyToManyField(to='URL', related_name='pdf_files')

    objects = PDFFileManager()

    def __unicode__(self):
        return self.name

    def links_number(self):
        return self.urls.count()


class URL(models.Model):
    link = models.URLField(unique=True)
    is_alive = models.NullBooleanField()

    def __unicode__(self):
        return self.link
