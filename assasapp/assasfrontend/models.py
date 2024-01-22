from django.db import models
import uuid

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    uuid = str(uuid.uuid4())
    document = models.FileField(upload_to='documents/'+uuid)
    uploaded_at = models.DateTimeField(auto_now_add=True)
