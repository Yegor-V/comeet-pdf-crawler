from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='PDFFile',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    )
                ),
                (
                    'name',
                    models.CharField(
                        max_length=200,
                        unique=True,
                    )
                ),
            ],
        ),
        migrations.CreateModel(
            name='URL',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    )
                ),
                (
                    'link',
                    models.URLField(unique=True),
                ),
                (
                    'is_alive',
                    models.NullBooleanField(),
                ),
            ],
        ),
        migrations.AddField(
            model_name='pdffile',
            name='urls',
            field=models.ManyToManyField(
                related_name='pdf_files',
                to='pdfurls.URL'
            ),
        ),
    ]
