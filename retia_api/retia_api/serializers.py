from rest_framework import serializers
from .models import Device

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Device
        fields=['hostname','mgmt_ipaddr', 'port', 'username', 'secret', 'created_at', 'modified_at']