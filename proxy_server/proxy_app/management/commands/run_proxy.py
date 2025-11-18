from django.core.management.base import BaseCommand
from mitmproxy.tools.main import mitmdump

class Command(BaseCommand):
    help = 'Run the mitmproxy with complex.py script'

    def handle(self, *args, **options):
        mitmdump(args=[
            '-s', 'complex.py',
            '--listen-port', '8080',
            '--set', 'ssl_insecure=true'
        ])