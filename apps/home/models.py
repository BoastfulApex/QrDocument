from django.db import models
from django.contrib.auth.models import User
import uuid


class DocsObjects(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(null=True)
    qrcode = models.ImageField(null=True)
    code = models.CharField(max_length=100, null=True, blank=True)

    @property
    def PhotoURL(self):
        try:
            return self.qrcode.url
        except:
            return ''
