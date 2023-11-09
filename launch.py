import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()

from integrations.aws.s3 import Client  # noqa: E402
from photo.tests.factories import ContestFactory, ContestSubmissionFactory  # noqa: E402

client = Client()
client.create_bucket()

contests = ContestFactory.create_batch(5)

for contest in contests:
    ContestSubmissionFactory.create_batch(5, contest=contest)
