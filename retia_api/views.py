from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Device, Detector
from .serializers import DeviceSerializer, DetectorSerializer
from retia_api.operation import *



@api_view(['GET','POST'])
def devices(request):
    if request.method=='GET':
        device=Device.objects.all()
        serializer=DeviceSerializer(instance=device, many=True)
        devices_data=serializer.data
        for i, device_data in enumerate(devices_data):
            del devices_data[i]["username"]
            del devices_data[i]["secret"]
            del devices_data[i]["port"]
            del devices_data[i]["created_at"]
            del devices_data[i]["modified_at"]
        return Response(serializer.data)
    elif request.method=='POST':
        device=Device.objects.all()
        serializer=DeviceSerializer(data=request.data)
        if serializer.is_valid():
            conn=check_device_connection(conn_strings={"ipaddr":request.data["mgmt_ipaddr"], "port": request.data["port"],'credential':(request.data["username"], request.data["secret"])})
            if not conn.status_code == 200:
                return Response(status=conn.status_code, data=conn.text)            
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": serializer.errors})

        
@api_view(['GET','PUT','DELETE'])
def device_detail(request, hostname):
    # Check whether device exist in database
    try:
        device=Device.objects.get(pk=hostname)
    except Device.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Connection string to device
    conn_strings={"ipaddr":device.mgmt_ipaddr, "port":device.port, 'credential':(device.username, device.secret)}

    # Handle request methods
    if request.method=='GET':
        # Update device hosname based on retia database
        device_cuurent_hostname=getHostname(conn_strings=conn_strings)["body"]
        if not device.hostname == device_cuurent_hostname:
            setHostname(conn_strings=conn_strings, req_to_change={"hostname":device.hostname})

        serializer=DeviceSerializer(instance=device)
        data=dict(serializer.data)
        data["sotfware_version"]=getVersion(conn_strings=conn_strings)["body"]
        data["login_banner"]=getLoginBanner(conn_strings=conn_strings)["body"]
        data["motd_banner"]=getMotdBanner(conn_strings=conn_strings)["body"]
        return JsonResponse(data)
    
    elif request.method=='PUT':
        serializer=DeviceSerializer(instance=device, data=request.data)
        if serializer.is_valid():
            if not hostname == serializer.initial_data['hostname']:
                device.delete()
            serializer.save()
            res_hostname=setHostname(conn_strings=conn_strings, req_to_change={"hostname":request.data["hostname"]})
            res_loginbanner=setLoginBanner(conn_strings=conn_strings, req_to_change={"login_banner":request.data["login_banner"]})
            res_motdbanner=setMotdBanner(conn_strings=conn_strings, req_to_change={"motd_banner":request.data["motd_banner"]}) 
            return Response({"code": {"hostname_change":res_hostname["code"], "loginbanner_change": res_loginbanner["code"], "motdbanner_change": res_motdbanner["code"]}})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='DELETE':
        device.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])  
def interfaces(request, hostname):
    # Check whether device exist in database
    try:
        device=Device.objects.get(pk=hostname)
    except Device.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Connection string to device
    conn_strings={"ipaddr":device.mgmt_ipaddr, "port":device.port, 'credential':(device.username, device.secret)}

    if request.method=='GET':
        return Response(getInterfaceList(conn_strings=conn_strings))
    
@api_view(['GET', 'PUT'])
def interface_detail(request, hostname, name):
    # Check whether device exist in database
    try:
        device=Device.objects.get(pk=hostname)
    except Device.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Connection string to device
    conn_strings={"ipaddr":device.mgmt_ipaddr, "port":device.port, 'credential':(device.username, device.secret)}
    
    # Handle request methods
    if request.method=='GET':
        return Response(getInterfaceDetail(conn_strings=conn_strings, req_to_show={"name":name}))
    elif request.method=='PUT':
        return Response(setInterfaceDetail(conn_strings=conn_strings, req_to_change=request.data))
        

@api_view(['GET','PUT'])
def static_route(request, hostname):
    # Check whether device exist in database
    try:
        device=Device.objects.get(pk=hostname)
    except Device.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Connection string to device
    conn_strings={"ipaddr":device.mgmt_ipaddr, "port":device.port, 'credential':(device.username, device.secret)}

    # Handle request methods
    if request.method=="GET":
        return Response(getStaticRoute(conn_strings=conn_strings))
    if request.method=="PUT":
        return Response(setStaticRoute(conn_strings=conn_strings, req_to_change=request.data))
    
@api_view(['GET','POST','DELETE'])
def ospf_processes(request, hostname):
    # Check whether device exist in database
    try:
        device=Device.objects.get(pk=hostname)
    except Device.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Connection string to device
    conn_strings={"ipaddr":device.mgmt_ipaddr, "port":device.port, 'credential':(device.username, device.secret)}

    if request.method=="GET":
        return Response(getOspfProcesses(conn_strings=conn_strings))
    elif request.method=="POST":
        return Response(createOspfProcess(conn_strings=conn_strings, req_to_create={"id": request.data["id"]}))

@api_view(['GET','PUT','DELETE'])
def ospf_process_detail(request, hostname, id):
    # Check whether device exist in database
    try:
        device=Device.objects.get(pk=hostname)
    except Device.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Connection string to device
    conn_strings={"ipaddr":device.mgmt_ipaddr, "port":device.port, 'credential':(device.username, device.secret)}

    if request.method=="GET":
        return Response(getOspfProcessDetail(conn_strings=conn_strings, req_to_show={"id":id}))
    elif request.method=="PUT":
        return Response(setOspfProcessDetail(conn_strings=conn_strings, req_to_change=request.data))
    elif request.method=="DELETE":
        return Response(delOspfProcess(conn_strings=conn_strings, req_to_del={"id":id}))
    
@api_view(['GET','POST'])
def acls(request, hostname):
    # Check whether device exist in database
    try:
        device=Device.objects.get(pk=hostname)
    except Device.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Connection string to device
    conn_strings={"ipaddr":device.mgmt_ipaddr, "port":device.port, 'credential':(device.username, device.secret)}

    if request.method=="GET":
        return Response(getAclList(conn_strings=conn_strings))
    elif request.method=="POST":
        return Response(createAcl(conn_strings=conn_strings, req_to_create={"name":request.data["name"]}))

@api_view(['GET','PUT','DELETE'])
def acl_detail(request, hostname, name):
    # Check whether device exist in database
    try:
        device=Device.objects.get(pk=hostname)
    except Device.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Connection string to device
    conn_strings={"ipaddr":device.mgmt_ipaddr, "port":device.port, 'credential':(device.username, device.secret)}

    if request.method=="GET":
        return Response(getAclDetail(conn_strings=conn_strings, req_to_show={"name":name}))
    elif request.method=="PUT":
        return Response(setAclDetail(conn_strings=conn_strings, req_to_change=request.data))
    elif request.method=="DELETE":
        return Response(delAcl(conn_strings=conn_strings, req_to_del={"name":name}))

@api_view(['GET','POST'])
def detectors(request):
    detector=Detector.objects.all()
    if request.method=='GET':
        serializer=DetectorSerializer(instance=detector, many=True)
        detector_instances=serializer.data
        detector_instance_name=[]
        for detector_instance in detector_instances:
            detector_instance_name.append(detector_instance["device"])
        return Response(detector_instance_name)
    elif request.method=='POST':
        serializer=DetectorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": serializer.errors})


@api_view(['GET', 'PUT',"DELETE"])
def detector_detail(request, device):
    # Check whether detector exist in database
    try:
        detector=Detector.objects.get(pk=device)
    except Detector.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Check whether device exist in database
    try:
        device=Device.objects.get(pk=device)
    except Device.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Connection string to device
    conn_strings={"ipaddr":device.mgmt_ipaddr, "port":device.port, 'credential':(device.username, device.secret)}

    if request.method=='GET':
        device_sync_status=check_device_detector_config(conn_strings=conn_strings, req_to_check={"device_interface_to_server": detector.device_interface_to_server, "device_interface_to_filebeat":detector.device_interface_to_filebeat, "filebeat_host": detector.filebeat_host, "filebeat_port":detector.filebeat_port})
        serializer=DetectorSerializer(instance=detector)
        detector_data={"sync":device_sync_status, "data":serializer.data}
        return Response(detector_data)
    
    elif request.method=='PUT':
        serializer=DetectorSerializer(instance=detector, data=request.data)
        if serializer.is_valid():
            if not device == serializer.initial_data["device"]:
                device_operation_result=del_device_detector_config(conn_strings=conn_strings)
                if device_operation_result["code"]==204:
                    detector.delete()
                else:
                    return Response(status=status.http_502_BAD_GATEWAY,data={"error":device_operation_result["body"]})
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method=='DELETE':
        device_operation_result=del_device_detector_config(conn_strings=conn_strings)
        if device_operation_result["code"]==204:
            detector.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.http_502_BAD_GATEWAY, data=device_operation_result)

@api_view(['PUT'])
def detector_sync(request, device):
    # Check whether detector exist in database
    try:
        detector=Detector.objects.get(pk=device)
    except Detector.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Check whether device exist in database
    try:
        device=Device.objects.get(pk=device)
    except Device.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Connection string to device
    conn_strings={"ipaddr":device.mgmt_ipaddr, "port":device.port, 'credential':(device.username, device.secret)}

    if request.method=='PUT':
        return Response(sync_device_detector_config(conn_strings=conn_strings, req_to_change={"device_interface_to_filebeat":detector.device_interface_to_filebeat, "device_interface_to_server": detector.device_interface_to_server, "filebeat_host": detector.filebeat_host, "filebeat_port":detector.filebeat_port}))


# BUAT FUNGSI SECURITIY (username, pass encryption, write, erase)