import os
from datetime import timedelta

from django.core.wsgi import get_wsgi_application
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()

from integrations.aws.s3 import Client  # noqa: E402
from photo.tests.factories import ContestFactory, ContestSubmissionFactory  # noqa: E402

client = Client()
client.create_bucket()

contests = ContestFactory.create_batch(5)

for contest in contests:
    ContestSubmissionFactory.create_batch(5, contest=contest)

time = timezone.now()
voting = ContestFactory(
    upload_phase_start=time - timedelta(days=3),
)

ContestSubmissionFactory.create_batch(10, contest=voting)

voting.upload_phase_end = time - timedelta(days=2)
voting.voting_phase_end = time + timedelta(days=1)
voting.save()

closed = ContestFactory(
    upload_phase_start=time - timedelta(days=3),
)

ContestSubmissionFactory.create_batch(10, contest=closed)
closed.upload_phase_end = time - timedelta(days=2)
closed.voting_phase_end = time - timedelta(days=1)
closed.save()
