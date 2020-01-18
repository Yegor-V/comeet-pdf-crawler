API endpoints:

1. Uploading a PDF document:
   POST /api/v1/pdf_files/
   HEADERS: Content-Type: multipart/form-data
   BODY: "file": <PDF file>

2. Set of all the of documents that were uploaded:
   GET /api/v1/pdf_files/

3. Set of URLs for a specific document:
   GET /api/v1/pdf_files/{document_id}/urls/

4. Set of all URLs found, including the number of documents that contained the URL
   GET /api/v1/urls/

Assumptions made:

Assume that file parsing, extracting links from it and saving them to DB is
fast enough, so it is done within synchronously. If it will appear that files
are to big, files parsing should be done asynchronously.

Checking links should be done after user had received response, as it might be
slow and here we depend on external resources.

Checking whether link is alive is based on HTTP code returned by the server.

Checking is done using just threading module. Celery, or other third party
libraries could be used, but that seems like overkill for me. If application
will scale, transition to celery seems like a good option.

Assuming that URLs should be checked only once - when file is uploaded.
In future it is very likely that business will add a requirement to recheck
links periodically.

Assuming that chances of the race condition in create_from_file method in
PDFFileManager class, when same URL was created when we were checking for
URLs that already exist as very low. If it is not true, we should switch to
safer variant - for example, Postgres UPSERT.

Used django test instead of pytest - the industry standard - as it seems more
convenient for python 2.7 project.

There are 2 good ways of structuring projects - by responsibility first and
then by business value and visa versa. I've chosen latter as it is more
convenient for django projects.


Steps to be made next:
 - finish covering all functionality with tests
 - deploy
 - dockerize
 - adding docs
 - adding CI
 - switching to python 3! :)
