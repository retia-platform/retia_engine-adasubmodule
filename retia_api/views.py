from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Device, Detector
from .serializers import DeviceSerializer, DetectorSerializer
from retia_api.operation import *
from apscheduler.schedulers.background import BackgroundScheduler
from retia_api.nescient import core
from retia_api.elasticclient import get_netflow_resampled
from retia_api.logging import activity_log


def logging():
    pass

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
                activity_log("error", request.data["hostname"], "device", conn.text)
                return Response(status=conn.status_code, data=conn.text)            
            serializer.save()
            activity_log("info", request.data["hostname"], "device", "Device %s added successfully"%(request.data["hostname"]))
            return Response(status=status.HTTP_201_CREATED)
        else:
            activity_log("error", request.data["hostname"], "device", "Device %s creation error: %s."%(request.data['hostname'], serializer.errors))
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
        # Tambah up time, up/down status

        return Response(data)
    
    elif request.method=='PUT':
        serializer=DeviceSerializer(instance=device, data=request.data)
        if serializer.is_valid():
            if not hostname == serializer.initial_data['hostname']:
                device.delete()
            serializer.save()
            res_hostname=setHostname(conn_strings=conn_strings, req_to_change={"hostname":request.data["hostname"]})
            res_loginbanner=setLoginBanner(conn_strings=conn_strings, req_to_change={"login_banner":request.data["login_banner"]})
            res_motdbanner=setMotdBanner(conn_strings=conn_strings, req_to_change={"motd_banner":request.data["motd_banner"]})
            response_body={"code": {"hostname_change":res_hostname["code"], "loginbanner_change": res_loginbanner["code"], "motdbanner_change": res_motdbanner["code"]}}
            activity_log("info", hostname, "device", "Device %s edited successfully. Sync status: %s"%(hostname, response_body))
            return Response(response_body)
        else:
            activity_log("error", hostname, "device", "Device %s edit error: %s"%(hostname, serializer.errors))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='DELETE':
        device.delete()
        activity_log("info", hostname, "device", "Device %s deleted succesfully"%(hostname))
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
        result=setInterfaceDetail(conn_strings=conn_strings, req_to_change=request.data)

        if result["code"] == 200  or result["code"]==204:
            activity_log("info", hostname, "interface", "Interface %s config saved: %s"%(name, request.data))
        else:
            activity_log("error", hostname, "interface", "Interface %s config error: %s"%(name, result['body']))

        return Response(result)
        

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
    elif request.method=="PUT":
        result=setStaticRoute(conn_strings=conn_strings, req_to_change=request.data)

        if result["code"] == 200  or result["code"]==204:
            activity_log("info", hostname, "static route", "Static route config saved: %s."%(request.data))
        else:
            activity_log("error", hostname, "static route", "Static route config error: %s."%(result['body']))

        return Response(result)
    
@api_view(['GET','POST'])
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
        result=createOspfProcess(conn_strings=conn_strings, req_to_create={"id": request.data["id"]})

        if result["code"] == 200  or result["code"]==201:
            activity_log("info", hostname, "OSPF", "OSPF Process %s created."%(request.data['id']))
        else:
            activity_log("error", hostname, "OSPF", "OSPF Process %s creation error: %s."%(request.data['id'], result['body']))

        return Response(result)

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
        result=setOspfProcessDetail(conn_strings=conn_strings, req_to_change=request.data)

        if result["code"] == 200  or result["code"]==204:
            activity_log("info", hostname, "OSPF", "OSPF process %s config saved: %s."%(id, request.data))
        else:
            activity_log("error", hostname, "OSPF", "OSPF process %s config error: %s."%(id, result['body']))

        return Response(result)
    elif request.method=="DELETE":
        result=delOspfProcess(conn_strings=conn_strings, req_to_del={"id":id})

        if result["code"] == 200  or result["code"]==204:
            activity_log("info", hostname, "OSPF", "OSPF process %s deleted."%(id))
        else:
            activity_log("error", hostname, "OSPF", "OSPF process %s deletion error: %s."%(id, result['body']))

        return Response(result)
    
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
        result=createAcl(conn_strings=conn_strings, req_to_create={"name":request.data["name"]})

        if result["code"] == 200  or result["code"]==204:
            activity_log("info", hostname, "ACL", "ACL %s created."%(request.data['name']))
        else:
            activity_log("error", hostname, "ACL", "ACL %s creation error: %s."%(request.data['name'], result['body']))

        return Response(result)

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
        result=setAclDetail(conn_strings=conn_strings, req_to_change=request.data)

        if result["code"] == 200  or result["code"]==204:
            activity_log("info", hostname, "ACL", "ACL %s config saved: %s"%(name, request.data))
        else:
            activity_log("error", hostname, "ACL", "ACL %s config error: %s"%(name, result['body']))
        
        return Response(result)
    
    elif request.method=="DELETE":
        result=delAcl(conn_strings=conn_strings, req_to_del={"name":name})

        if result["code"] == 200  or result["code"]==204:
            activity_log("info", hostname, "ACL", "ACL %s deleted"%(name))
        else:
            activity_log("error", hostname, "ACL", "ACL %s deletion error: %s"%(name, result['body']))
        return Response()

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
            activity_log("info", 'retia-engine', "detector", "Detector %s added successfully"%(request.data["device"]))
            return Response(status=status.HTTP_201_CREATED)
        else:
            activity_log("info", 'retia-engine', "detector", "Detector %s addition error: %s."%(request.data["device"], serializer.errors))
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
                    activity_log("error", 'retia-engine', "detector", "Detector %s edit error: %s."%(device, device_operation_result['body']))
                    return Response(status=status.http_502_BAD_GATEWAY,data={"error":device_operation_result["body"]})
            serializer.save()
            activity_log("info", 'retia-engine', "detector", "Detector %s edited successfully."%(device))
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            activity_log("error", 'retia-engine', "detector", "Detector %s edit error: %s."%(device, serializer.errors))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method=='DELETE':
        device_operation_result=del_device_detector_config(conn_strings=conn_strings)
        if device_operation_result["code"]==204:
            detector.delete()
            activity_log("error", 'retia-engine', "detector", "Detector %s deleted successfully."%(device))
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            activity_log("error", 'retia-engine', "detector", "Detector %s deletion error: %s."%(device, device_operation_result))
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
        result=sync_device_detector_config(conn_strings=conn_strings, req_to_change={"device_interface_to_filebeat":detector.device_interface_to_filebeat, "device_interface_to_server": detector.device_interface_to_server, "filebeat_host": detector.filebeat_host, "filebeat_port":detector.filebeat_port})

        if result["code"] == 200  or result["code"]==204:
            activity_log("info", 'retia-engine', "detector", "Detector netflow device %s synced."%(device))
        else:
            activity_log("error", 'retia-engine', "detector", "Detector netflow device %s failed to sync."%(device, result['body']))

        return Response(result)

@api_view(['PUT'])
def detector_start(request, device):    
    def detector_job(detector_instance):
        print("\n\n\n\n\n----------------------------------------------------------------------------------")
        core(get_netflow_resampled("now", detector_instance.sampling_interval, detector_instance.elastic_host, detector_instance.elastic_index), detector_instance)
    
    # Check whether detector exist in database
    try:
        detector=Detector.objects.get(pk=device)
    except Detector.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # if request.method=='PUT':
    #     scheduler=BackgroundScheduler()
    #     scheduler.add_job(func=detector_job, args=[detector], trigger="cron", seconds=detector.sampling_interval, id=detector.device,max_instances=1, replace_existing=True)
    #     scheduler.start()
    scheduler=BackgroundScheduler()
    scheduler.add_job(func=detector_job, args=[detector], trigger="cron", second=detector.sampling_interval, id=str(detector.device), max_instances=1, replace_existing=True)
    scheduler.start()
    # try:
    #     scheduler=BackgroundScheduler()
    #     scheduler.add_job(func=detector_job, args=[detector], trigger="cron", second="*/%s"%(detector.sampling_interval), id=str(detector.device), max_instances=1, replace_existing=True)
    #     scheduler.start()
    # except Exception as e:
    #     print(e)

@api_view(['GET'])
def monitoring_buildinfo(request):
    if request.method=='GET':
        return Response(data=getMonitorBuildinfo())

@api_view(['GET'])
def interface_in_throughput(request, hostname, name):
    # Check whether device exist in database
    try:
        device=Device.objects.get(pk=hostname)
    except Device.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        data=request.data
        return Response(data=getInterfaceInThroughput(device.mgmt_ipaddr, name, data['start_time'], data['end_time']))

@api_view(['GET'])
def interface_out_throughput(request, hostname, name):
    # Check whether device exist in database
    try:
        device=Device.objects.get(pk=hostname)
    except Device.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        data=request.data
        return Response(data=getInterfaceOutThroughput(device.mgmt_ipaddr, name, data['start_time'], data['end_time']))


# BUAT FUNGSI SECURITIY (username, pass encryption, write, erase)