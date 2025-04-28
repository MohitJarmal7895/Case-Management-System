@echo off
echo Starting Celery Worker and Beat...
start cmd /k "celery -A legal_management worker -l info"
start cmd /k "celery -A legal_management beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler"