from django.db import models

class Device(models.Model):
    hostname=models.CharField(max_length=63, primary_key=True)
    mgmt_ipaddr=models.CharField(max_length=15)
    port=models.IntegerField(default=443)
    username=models.CharField(max_length=16, default=None)
    secret=models.CharField(max_length=64, default=None)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.hostname
    

# class Log(models.Model):
#     target = models.CharField(max_length=200)
#     action = models.CharField(max_length=200)
#     status = models.CharField(max_length=200)
#     messages = models.CharField(max_length=255, blank=True)
#     time = models.DateTimeField(null=True)
#     user = models.CharField(max_length=200, default='Anonymous')

#     def __str__(self):
#         return "{} - {} - {}".format(self.target, self.action, self.status)

class Detector(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE, primary_key=True)
    device_interface_to_filebeat = models.CharField(max_length=200, default=None)
    device_interface_to_server=models.CharField(max_length=200, default=None)
    window_size = models.IntegerField(default=1)
    sampling_interval = models.IntegerField(default=20)
    elastic_host = models.GenericIPAddressField()
    elastic_index = models.CharField(max_length=255)
    filebeat_host = models.GenericIPAddressField()
    filebeat_port = models.BigIntegerField(default=50255)

    def __str__(self):
        return self.device.hostname
