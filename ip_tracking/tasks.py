# ip_tracking/tasks.py
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import RequestLog, SuspiciousIP

@shared_task
def detect_suspicious_ips():
    """
    Detect IPs with unusual behavior:
    - More than 100 requests/hour
    - Accessing sensitive paths (/admin, /login)
    """
    one_hour_ago = timezone.now() - timedelta(hours=1)

    # Aggregate requests in the past hour
    recent_requests = RequestLog.objects.filter(timestamp__gte=one_hour_ago)

    # Check for high request volume per IP
    ip_counts = {}
    for req in recent_requests:
        ip_counts[req.ip_address] = ip_counts.get(req.ip_address, 0) + 1

    for ip, count in ip_counts.items():
        if count > 100:
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                defaults={'reason': f"High request volume: {count} requests in the last hour"}
            )

    # Check for sensitive path access
    sensitive_paths = ['/admin', '/login']
    for req in recent_requests:
        if any(req.path.startswith(sp) for sp in sensitive_paths):
            SuspiciousIP.objects.get_or_create(
                ip_address=req.ip_address,
                defaults={'reason': f"Accessed sensitive path: {req.path}"}
            )
