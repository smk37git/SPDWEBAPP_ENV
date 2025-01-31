from django.core.management.base import BaseCommand
from AUTHENTICATE.utils import clean_existing_majors

class Command(BaseCommand):
    help = 'Cleans existing majors that contain profanity'

    def handle(self, *args, **kwargs):
        cleaned_count = clean_existing_majors()
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully cleaned majors. Removed {cleaned_count} inappropriate entries.'
            )
        )