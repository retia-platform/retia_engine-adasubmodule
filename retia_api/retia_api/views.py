from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .operation import *
from .models import Device
from .serializers import DeviceSerializer



@api_view(['GET','POST'])
def devices(request):
    if request.method=='GET':
        device=Device.objects.all()
        serializer=DeviceSerializer(instance=device, many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        serializer=DeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)


@api_view(['GET','PUT','DELETE'])
def device_detail(request, hostname):
    # Check whether device exist in database
    try:
        device=Device.objects.get(pk=hostname)
    except Device.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Connection string to device
    conn_strings={"ipaddr":device.mgmt_ipaddr, "port":"443", 'credential':(device.username, device.secret)}

    # Check device connectivity
    # ilanging kalo gabisa
    # conn=check_device_connection(conn_strings=conn_strings)
    # print(conn)


    # Update device hosname based on retia database
    device_cuurent_hostname=getHostname(conn_strings=conn_strings)["body"]
    if not device.hostname == device_cuurent_hostname:
        print("Hostname on %s manaually changed (%s), updating to RETIA's configuration"%(device.hostname, device_cuurent_hostname))
        setHostname(conn_strings=conn_strings, req_to_change={"hostname":device.hostname})

    # Handle request methods
    if request.method=='GET':
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
    conn_strings={"ipaddr":device.mgmt_ipaddr, "port":"443", 'credential':(device.username, device.secret)}

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
    conn_strings={"ipaddr":device.mgmt_ipaddr, "port":"443", 'credential':(device.username, device.secret)}
    
    # Handle request methods
    if request.method=='GET':
        return Response(getInterfaceDetail(conn_strings=conn_strings    , req_to_show={"name":name}))
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
    conn_strings={"ipaddr":device.mgmt_ipaddr, "port":"443", 'credential':(device.username, device.secret)}

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
    conn_strings={"ipaddr":device.mgmt_ipaddr, "port":"443", 'credential':(device.username, device.secret)}

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
    conn_strings={"ipaddr":device.mgmt_ipaddr, "port":"443", 'credential':(device.username, device.secret)}

    if request.method=="GET":
        return Response(getOspfProcessDetail(conn_strings=conn_strings, req_to_show={"id":id}))
    elif request.method=="PUT":
        return Response(setOspfProcessDetail(conn_strings=conn_strings, req_to_change=request.data))
    elif request.method=="DELETE":
        return Response(delOspfProcess(conn_strings=conn_strings, req_to_del={"id":id}))