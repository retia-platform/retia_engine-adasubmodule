from django.db import models

class Device(models.Model):
    hostname=models.CharField(max_length=63, primary_key=True)
    mgmt_ipaddr=models.CharField(max_length=15)
    port=models.IntegerField(max_length=5, default=443)
    username=models.CharField(max_length=16, default='retia')
    secret=models.CharField(max_length=64, default='retia00!')
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.hostname