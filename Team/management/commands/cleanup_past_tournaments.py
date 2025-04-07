from django.core.management.base import BaseCommand
from django.utils import timezone
from Team.models import Tournament
import datetime

class Command(BaseCommand):
    help = 'Deletes tournaments that ended more than 30 days ago.'

    def handle(self, *args, **options):
        current_date = timezone.now().date()
        threshold_date = current_date - datetime.timedelta(days=30)

        # Find tournaments that ended more than 30 days ago
        past_tournaments = Tournament.objects.filter(end_date__lt=threshold_date)

        if past_tournaments.exists():
            deleted_count = past_tournaments.count()
            past_tournaments.delete()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully deleted {deleted_count} past tournaments.')
            )
        else:
            self.stdout.write(
                self.style.WARNING('No past tournaments to delete.')
            )