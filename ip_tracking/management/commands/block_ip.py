from django.core.management.base import BaseCommand, CommandError
from ip_tracking.models import BlockedIP

class Command(BaseCommand):
    help = "This command adds an IP address to the BlockedIP model."

    def add_arguments(self, parser):
        parser.add_argument("ip_address", type=str, help="The IP address to block")

    def handle(self, *args, **kwargs):
        ip_address = kwargs["ip_address"]

        try:
            obj, created = BlockedIP.objects.get_or_create(ip_address=ip_address)
            if created:
                self.stdout.write(self.style.SUCCESS(f"IP {ip_address} has been blocked."))
            else:
                self.stdout.write(self.style.WARNING(f"IP {ip_address} is already blocked."))
        except Exception as e:
            raise CommandError(f"Error blocking IP {ip_address}: {e}")