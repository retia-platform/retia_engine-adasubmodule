from django.db import models
from retia_api.detector.utils import NetflowSlugs
from retia_api.operation import patchSomething

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

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None, *args, **kwargs):
    #     if update_fields is not None:
    #         try:
    #             if self.remove_netflow_config():
    #                 log = Log(target=self.device.ip_address, action="[Nescient] Remove Netflow Config",
    #                           status="Successful",
    #                           time=datetime.now(), user='Anonymous', messages="No Error")
    #                 log.save()
    #             else:
    #                 log = Log(target=self.device.ip_address, action="[Nescient] Remove Netflow Config",
    #                           status="Error",
    #                           time=datetime.now(), user='Anonymous', messages="Invalid Script")
    #                 log.save()
    #         except Exception as e:
    #             log = Log(target=self.device.ip_address, action="[Nescient] Remove Netflow Config", status="Exception",
    #                       time=datetime.now(),
    #                       user='Anonymous', messages=e.__str__()[0:255])
    #             log.save()
    #     try:
    #         if self.add_netflow_config():
    #             super(Detector, self).save(*args, **kwargs)
    #             log = Log(target=self.device.ip_address, action="[Nescient] Add Netflow Config", status="Successful",
    #                       time=datetime.now(), user='Anonymous', messages="No Error")
    #             log.save()
    #         else:
    #             log = Log(target=self.device.ip_address, action="[Nescient] Add Netflow Config", status="Error",
    #                       time=datetime.now(),
    #                       user='Anonymous', messages="Invalid Script")
    #             log.save()

    #     except Exception as e:
    #         log = Log(target=self.device.ip_address, action="[Nescient] Add Netflow Config", status="Exception",
    #                   time=datetime.now(),
    #                   user='Anonymous', messages=e.__str__()[0:255])
    #         log.save()

    # def delete(self, using=None, keep_parents=False, *args, **kwargs):
    #     try:
    #         if self.remove_netflow_config():
    #             log = Log(target=self.device.ip_address, action="[Nescient] Remove Netflow Config",
    #                       status="Successful",
    #                       time=datetime.now(), user='Anonymous', messages="No Error")
    #             log.save()
    #         else:
    #             log = Log(target=self.device.ip_address, action="[Nescient] Remove Netflow Config",
    #                       status="Error",
    #                       time=datetime.now(), user='Anonymous', messages="Invalid Script")
    #             log.save()
    #     except Exception as e:
    #         log = Log(target=self.device.ip_address, action="[Nescient] Remove Netflow Config", status="Exception",
    #                   time=datetime.now(),
    #                   user='Anonymous', messages=e.__str__()[0:255])
    #         log.save()
    #     super(Detector, self).delete(*args, **kwargs)

    # def __str__(self):
    #     return "{} {} {} {}".format(
    #         self.device.hostname, self.device_interface, self.window_size, self.sampling_interval)
