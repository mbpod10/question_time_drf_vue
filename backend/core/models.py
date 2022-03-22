from django.db import models


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # abstract true means that a table will not be created in the
    # database
    class Meta:
        abstract = True
