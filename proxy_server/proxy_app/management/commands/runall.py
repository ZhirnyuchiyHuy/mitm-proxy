
import subprocess
import time
import sys
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Run Django server and mitmproxy in parallel (using subprocess)'

    def handle(self, *args, **options):
        print("Starting Django + mitmproxy using subprocess...")

        # Запуск Django runserver
        django_process = subprocess.Popen([
            sys.executable, "manage.py", "runserver", "127.0.0.1:8000"
        ])

        # Запуск mitmproxy
        proxy_process = subprocess.Popen([
            sys.executable, "manage.py", "run_proxy"
        ])

        print("Django: http://127.0.0.1:8000")

        try:
            while True:
                if django_process.poll() is not None:
                    print("Django stopped. Stopping proxy...")
                    proxy_process.terminate()
                    break
                if proxy_process.poll() is not None:
                    print("Proxy stopped. Stopping Django...")
                    django_process.terminate()
                    break
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down both...")
            django_process.terminate()
            proxy_process.terminate()

        # Ждём завершения
        django_process.wait()
        proxy_process.wait()
        print("Both servers stopped.")