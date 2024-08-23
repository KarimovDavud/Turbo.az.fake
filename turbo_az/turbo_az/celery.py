from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Django ayarlarını default olarak yükle
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'turbo_az.settings')

app = Celery('turbo_az')

# Django ayarlarından Celery yapılandırmasını yükle
app.config_from_object('django.conf:settings', namespace='CELERY')

# Django uygulamalarını otomatik olarak yükle
app.autodiscover_tasks()
