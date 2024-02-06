import json, requests
from requests.exceptions import RequestException
from rest_framework import status
from apscheduler.schedulers.background import BackgroundScheduler
from retia_api.models import *


# Disable Sertificate Insecure Request Warning
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


def check_device_connection(conn_strings: dict)->dict:
    class response_custom:
        def __init__(self, err_code, err_text):
            self.status_code=err_code
            self.text=err_text
    
    target_url="https://%s:%s/restconf"%(conn_strings["ipaddr"], conn_strings["port"])
    try:
        response=requests.get(url=target_url, auth=conn_strings["credential"], headers={"Content-Type": "application/yang-data+json", "Accept": "application/yang-data+json"}, verify=False)
        return response
    except requests.exceptions.ConnectionError:
        err=response_custom(status.HTTP_404_NOT_FOUND, json.dumps({"error":"Device offline"}))
        return err
    

def getSomething(conn_strings: dict, path: str):
    class response_custom:
        def __init__(self, err_code, err_text):
            self.status_code=err_code
            self.text=err_text

    target_url="https://%s:%s/restconf/data/Cisco-IOS-XE-native:native%s"%(conn_strings["ipaddr"], conn_strings["port"], path)

    try:
        response= requests.get(url=target_url, auth=conn_strings["credential"], headers={"Content-Type": "application/yang-data+json", "Accept": "application/yang-data+json"}, verify=False)
        return response
    except requests.exceptions.ConnectionError:
        err=response_custom(status.HTTP_404_NOT_FOUND, json.dumps({"error":"Device offline"}))
        return err

def patchSomething(conn_strings: dict, path: str, body: str):
    class response_custom:
        def __init__(self, err_code, err_text):
            self.status_code=err_code
            self.text=err_text

    target_url="https://%s:%s/restconf/data/Cisco-IOS-XE-native:native%s"%(conn_strings["ipaddr"], conn_strings["port"], path)

    try:
        response=requests.patch(url=target_url, auth=conn_strings["credential"], headers={"Content-Type": "application/yang-data+json", "Accept": "application/yang-data+json"}, data=body, verify=False)
        return response
    except requests.exceptions.ConnectionError:
        err=response_custom(status.HTTP_404_NOT_FOUND, json.dumps({"error":"Device offline"}))
        return err

def putSomething(conn_strings: dict, path: str, body: str):
    class response_custom:
        def __init__(self, err_code, err_text):
            self.status_code=err_code
            self.text=err_text

    target_url="https://%s:%s/restconf/data/Cisco-IOS-XE-native:native%s"%(conn_strings["ipaddr"], conn_strings["port"], path)

    try:
        response=requests.put(url=target_url, auth=conn_strings["credential"], headers={"Content-Type": "application/yang-data+json", "Accept": "application/yang-data+json"}, data=body, verify=False)
        return response
    except requests.exceptions.ConnectionError:
        err=response_custom(status.HTTP_404_NOT_FOUND, json.dumps({"error":"Device offline"}))
        return err

def postSomething(conn_strings: dict, path: str, body: str):
    target_url="https://%s:%s/restconf/data/Cisco-IOS-XE-native:native%s"%(conn_strings["ipaddr"], conn_strings["port"], path)
    return requests.post(url=target_url, auth=conn_strings["credential"], headers={"Content-Type": "application/yang-data+json", "Accept": "application/yang-data+json"}, data=body, verify=False)

def delSomething(conn_strings: dict, path: str):
    target_url="https://%s:%s/restconf/data/Cisco-IOS-XE-native:native%s"%(conn_strings["ipaddr"], conn_strings["port"], path)
    return requests.delete(url=target_url, auth=conn_strings["credential"], headers={"Content-Type": "application/yang-data+json", "Accept": "application/yang-data+json"}, verify=False)


def getVersion(conn_strings: dict)->dict:
    response=getSomething(conn_strings, "/version")
    if len(response.text)>0:
        try:
            response_body=json.loads(response.text)["Cisco-IOS-XE-native:version"]
        except:
            response_body=json.loads(response.text)
    else:
        response_body={}
    return {"code": response.status_code, "body": response_body }

def getHostname(conn_strings: dict)->dict:
    response=getSomething(conn_strings, "/hostname")
    if len(response.text)>0:
        try: 
            response_body=json.loads(response.text)["Cisco-IOS-XE-native:hostname"]
        except:
            response_body=json.loads(response.text)
    else:
            response_body={}
    return {"code": response.status_code, "body": response_body }

def setHostname(conn_strings: dict, req_to_change: dict)->dict:
    body=json.dumps({"hostname": req_to_change["hostname"]})
    response=patchSomething(conn_strings, "/hostname", body)
    try:
        response_body=json.loads(response.text)
    except:
        response_body={}

    return {"code": response.status_code, "body": response_body}

def getLoginBanner(conn_strings: dict)->dict:
    response=getSomething(conn_strings, "/banner/login")

    if len(response.text)>0:
        try:
            response_body=json.loads(response.text)["Cisco-IOS-XE-native:login"]["banner"]
        except:
            response_body=json.loads(response.text)
    else:
        response_body={}
    return {"code": response.status_code, "body": response_body}

def setLoginBanner(conn_strings: dict, req_to_change: dict)->dict:
    if len(req_to_change["login_banner"])>0:
        body=json.dumps({"login": {"banner": req_to_change["login_banner"]}},indent=2)
        response=patchSomething(conn_strings, "/banner/login", body)
    else:
        response=delSomething(conn_strings, "/banner/login")

    try:
        response_body=json.loads(response.text)
    except:
        response_body={}

    return {"code": response.status_code, "body": response_body}

def getMotdBanner(conn_strings:dict)->dict:
    response=getSomething(conn_strings, "/banner/motd")

    if len(response.text)>0:
        try:
            response_body=json.loads(response.text)["Cisco-IOS-XE-native:motd"]["banner"]
        except:
            response_body=json.loads(response.text)
    else:
        response_body={}
    return {"code": response.status_code, "body": response_body}

def setMotdBanner(conn_strings:dict, req_to_change: dict)->dict:
    if len(req_to_change["motd_banner"])>0:
        body=json.dumps({"motd": {"banner": req_to_change["motd_banner"]}},indent=2)
        response=patchSomething(conn_strings, "/banner/motd", body)
    else:
        response=delSomething(conn_strings, "/banner/motd")
    try:
        response_body=json.loads(response.text)
    except:
        response_body={}
    return {"code": response.status_code, "body": response_body}

def getUsername(conn_strings: dict, req_to_change: dict)->dict:
    response=getSomething(conn_strings, "/username")

    if len(response.text)>0:
        try:
            response_body=json.loads(response.text)["Cisco-IOS-XE-native:username"]
        except:
            response_body=json.loads(response.text)
    else:
        response_body={}
    return {"code": response.status_code, "body": response_body}

def getPassEncryption(conn_strings:dict)->dict:
    response=getSomething(conn_strings, "/service/")
    if "password-encryption" in json.loads(response.text)["Cisco-IOS-XE-native:service"]:
        response_body="true"
    else:
        response_body="false"
    return {"code": response.status_code, "body": response_body}

def setPassEncryption(conn_strings, req_to_change: dict):
    if req_to_change["password-encryption"]=="true":
        body=json.dumps({"Cisco-IOS-XE-native:service": {"password-encryption":[None]}})
        response=patchSomething(conn_strings, "/service", body)
    elif req_to_change["password-encryption"]=="false" and getPassEncryption(conn_strings)["body"]=="true":
        response=delSomething(conn_strings, "/service/password-encryption")

    try:
        response_body=json.loads(response.text)
    except:
        response_body={}

    return {"code": response.status_code, "body": response_body}

def getInterfaceList(conn_strings:dict)->dict:
    class response_custom:
        def __init__(self, err_code, err_text):
            self.status_code=err_code
            self.text=err_text

    target_url="https://%s:%s/restconf/data/ietf-interfaces:interfaces/interface?fields=name"%(conn_strings["ipaddr"], conn_strings["port"])

    try:
        response=requests.get(url=target_url, auth=conn_strings["credential"], headers={"Content-Type": "application/yang-data+json", "Accept": "application/yang-data+json"}, verify=False)
    except requests.exceptions.ConnectionError:
        err=response_custom(status.HTTP_404_NOT_FOUND, json.dumps({"error":"Device offline"}))
        response=err

    if len(response.text)>0:
        try:
            response_body_interface_list=json.loads(response.text)["ietf-interfaces:interface"]
            response_body=[]
            for interface_name in response_body_interface_list:
                response_body.append(interface_name["name"])
        except:
            response_body=json.loads(response.text)
    else:
        response_body = {}

    return {"code" : response.status_code, "body" : response_body}

def getInterfaceDetail(conn_strings: dict, req_to_show: dict)->dict:
    class response_custom:
        def __init__(self, err_code, err_text):
            self.status_code=err_code
            self.text=err_text
    target_url="https://%s:%s/restconf/data/ietf-interfaces:interfaces/interface=%s"%(conn_strings["ipaddr"], conn_strings["port"], req_to_show["name"])

    try:
        response=requests.get(url=target_url, auth=conn_strings["credential"], headers={"Content-Type": "application/yang-data+json", "Accept": "application/yang-data+json"}, verify=False)
    except requests.exceptions.ConnectionError:
        err=response_custom(status.HTTP_404_NOT_FOUND, json.dumps({"error":"Device offline"}))
        response=err

    if len(response.text)>0:
        try:
            response_body={}
            interface_data=json.loads(response.text)["ietf-interfaces:interface"]
            response_body={"name":interface_data["name"], "type":interface_data["type"], "enabled": interface_data["enabled"], "ip":interface_data["ietf-ip:ipv4"]["address"][0]["ip"], "netmask":interface_data["ietf-ip:ipv4"]["address"][0]["netmask"]}
        except:
            response_body=json.loads(response.text)
    else:
        response_body={}
    return {"code" : response.status_code, "body" : response_body}

def setInterfaceDetail(conn_strings:dict, req_to_change: dict)->dict:
    class response_custom:
        def __init__(self, err_code, err_text):
            self.status_code=err_code
            self.text=err_text

    target_url="https://%s:%s/restconf/data/ietf-interfaces:interfaces/interface=%s"%(conn_strings["ipaddr"], conn_strings["port"], req_to_change["name"])

    try:
        try:
            int_type=getInterfaceDetail(conn_strings, {"name":req_to_change["name"]})["body"]["type"]
        except:
            int_type=None
        body=json.dumps({"ietf-interfaces:interface":{"name":req_to_change["name"], "type": int_type, "enabled": req_to_change["enabled"], "ietf-ip:ipv4": {"address":[{"ip":req_to_change["ip"], "netmask":req_to_change["netmask"]}]},"ietf-ip:ipv6":{}}}, indent=2)
        response=requests.put(url=target_url, auth=conn_strings["credential"], headers={"Content-Type": "application/yang-data+json", "Accept": "application/yang-data+json"}, verify=False, data=body)
    except requests.exceptions.ConnectionError:
        err=response_custom(status.HTTP_404_NOT_FOUND, json.dumps({"error":"Device offline"}))
        response=err

    try:
        response_body=json.loads(response.text)
    except:
        response_body={}
    return {"code": response.status_code, "body": response_body}

def getStaticRoute(conn_strings: dict)->dict:
    response=getSomething(conn_strings, "/ip/route/ip-route-interface-forwarding-list")
    if len(response.text)>0:
        try:
            response_body=json.loads(response.text)["Cisco-IOS-XE-native:ip-route-interface-forwarding-list"]
        except:
            response_body=json.loads(response.text)
    else:
        response_body={}
    return {"code": response.status_code, "body": response_body}

def setStaticRoute(conn_strings: dict, req_to_change: list)->dict:
    body=json.dumps({"Cisco-IOS-XE-native:route":{"ip-route-interface-forwarding-list": req_to_change}}, indent=2)
    response=putSomething(conn_strings, "/ip/route", body )
    try:
        response_body=json.loads(response.text)
    except:
        response_body={}
    return {"code": response.status_code, "body": response_body}

def getOspfProcesses(conn_strings: dict)->list:
    response=getSomething(conn_strings, "/router/Cisco-IOS-XE-ospf:router-ospf/ospf/process-id?fields=id")
    if len(response.text)>0:
        try:
            router_id=json.loads(response.text)["Cisco-IOS-XE-ospf:process-id"]
            response_body=[]
            for id in router_id:
                response_body.append(id["id"])
        except:
            response_body=json.loads(response.text)
    else:
        response_body=[]
    return {"code": response.status_code, "body": response_body}

def createOspfProcess(conn_strings: dict, req_to_create: dict):
    body=json.dumps({"Cisco-IOS-XE-ospf:process-id":{"id": req_to_create["id"]}}, indent=2)
    response=postSomething(conn_strings, "/router/Cisco-IOS-XE-ospf:router-ospf/ospf/", body)
    try:
        response_body=json.loads(response.text)
    except:
        response_body={}
    return {"code": response.status_code, "body": response_body}

def delOspfProcess(conn_strings: dict, req_to_del:dict)->list:
    response=delSomething(conn_strings, "/router/Cisco-IOS-XE-ospf:router-ospf/ospf/process-id=%s"%(req_to_del["id"]))
    try:
        response_body=json.loads(response.text)
    except:
        response_body={}
    return {"code": response.status_code, "body": response_body}

def getOspfProcessDetail(conn_strings: dict, req_to_show: dict)->dict:
    response=getSomething(conn_strings, "/router/Cisco-IOS-XE-ospf:router-ospf/ospf/process-id=%s"%(req_to_show["id"]))
    if len(response.text)>0:
        try:
            response_body=json.loads(response.text)["Cisco-IOS-XE-ospf:process-id"]
            if "default-information" in response_body:
                response_body["default-information-originate"]=True
            else:
                response_body["default-information-originate"]=False
            del response_body["default-information"]

            if "redistribute" in response_body:
                response_body["redistribute"]=list(response_body["redistribute"].keys())
            
            if "passive-interface" in response_body:
                response_body["passive-interface"]=response_body["passive-interface"]["interface"]
        except:
            response_body=json.loads(response.text)
    else:
        response_body={}
    return {"code": response.status_code, "body": response_body}

def setOspfProcessDetail(conn_strings: dict, req_to_change: dict)->dict:
    body={"Cisco-IOS-XE-ospf:process-id":{"id":req_to_change["id"], "network":req_to_change["network"], "passive-interface": {"interface": req_to_change["passive-interface"]}}}
    
    if req_to_change["default-information-originate"]==True:
        body["Cisco-IOS-XE-ospf:process-id"]["default-information"]={"originate":{}}

    if len(req_to_change["redistribute"])>0:
        body["Cisco-IOS-XE-ospf:process-id"]["redistribute"]={}
        for r in req_to_change["redistribute"]:
            body["Cisco-IOS-XE-ospf:process-id"]["redistribute"][r]={}
            
    body=json.dumps(body)
    response=putSomething(conn_strings, "/router/Cisco-IOS-XE-ospf:router-ospf/ospf/process-id=%s"%(req_to_change["id"]), body)

    try:
        response_body=json.loads(response.text)
    except:
        response_body={}
        
    body=json.dumps(body, indent=2)

    return {"code": response.status_code, "body": response_body}

def getAclList(conn_strings: dict)->dict:
    response=getSomething(conn_strings=conn_strings, path="/ip/access-list/standard?fields=name")
    if len(response.text)>0:
        try:
            response_body=[]
            acls=json.loads(response.text)["Cisco-IOS-XE-acl:standard"]
            for acl in acls:
                response_body.append(acl["name"])
        except:
            response_body=json.loads(response.text)
    else:
        response_body={}
    return {"code": response.status_code, "body": response_body}

def createAcl(conn_strings: dict, req_to_create: dict)->dict:
    body=json.dumps({"Cisco-IOS-XE-acl:standard": [{"name": req_to_create["name"]}]}, indent=2)
    response=postSomething(conn_strings, "/ip/access-list", body)
    try:
        response_body=json.loads(response.text)
    except:
        response_body={}
    return {"code": response.status_code, "body": response_body}

def getAclDetail(conn_strings: dict, req_to_show: dict)->dict:
    response=getSomething(conn_strings=conn_strings, path="/ip/access-list/standard=%s"%(req_to_show["name"]))
    if len(response.text)>0:
        try:
            acl_data=json.loads(response.text)["Cisco-IOS-XE-acl:standard"]
            if "access-list-seq-rule" in acl_data:
                sequences=[]
                for acl_sequence in acl_data["access-list-seq-rule"]:
                    sequence=acl_sequence["sequence"]
                    action="permit" if "permit" in acl_sequence else "deny"
                    prefix=acl_sequence[action]["std-ace"]["ipv4-prefix"] if "ipv4-prefix" in acl_sequence[action]["std-ace"] else "any"
                    mask=acl_sequence[action]["std-ace"]["mask"] if "mask" in acl_sequence[action]["std-ace"] else None
                    sequences.append({"sequence":sequence, "action": action, "prefix": prefix, "wildcard": mask})
                response_body={"name":acl_data["name"], "rules":sequences}
            else:
                response_body={"name":acl_data["name"]}
        except:
            response_body=json.loads(response.text)
    else:
        response_body={}

    return {"code": response.status_code, "body": response_body}

def setAclDetail(conn_strings: dict, req_to_change: dict)->dict:
    rules=[]
    for rule in req_to_change["rules"]:
        if rule["wildcard"]:
            rules.append({"sequence":rule["sequence"], rule["action"]:{"std-ace":{"ipv4-prefix": rule["prefix"], "mask": rule["wildcard"]}}})
        else:
            rules.append({"sequence":rule["sequence"], rule["action"]:{"std-ace":{"ipv4-prefix": rule["prefix"]}}})
    body=json.dumps({"Cisco-IOS-XE-acl:standard":{"name":req_to_change["name"],"access-list-seq-rule":rules}})

    response=putSomething(conn_strings, "/ip/access-list/standard=%s"%(req_to_change["name"]), body)
    try:
        response_body=json.loads(response.text)
    except:
        response_body={}
    body=json.dumps(body, indent=2)

    return {"code": response.status_code, "body": response_body}


def delAcl(conn_strings: dict, req_to_del:dict)->list:
    response=delSomething(conn_strings, "/ip/access-list/standard=%s"%(req_to_del["name"]))
    try:
        response_body=json.loads(response.text)
    except:
        response_body={}
    return {"code": response.status_code, "body": response_body}
    
    
def check_device_detector_config(conn_strings:dict, req_to_check:dict)->dict:
    # Check flow record, exporter, monitor configuration
    conn_check=check_device_connection(conn_strings=conn_strings)
    record_config_current=getSomething(conn_strings, "/flow/record=RETIA_RECORD")
    exporter_config_current=getSomething(conn_strings, "/flow/exporter=RETIA_EXPORTER")
    monitor_config_current=getSomething(conn_strings, "/flow/monitor=RETIA_MONITOR")
    interfaces_current=getSomething(conn_strings, "/interface")

    if conn_check.status_code==404:
        return {"synced":None, "status":"Device offline"}
    elif record_config_current.status_code==404 or exporter_config_current==404 or monitor_config_current==404 or interfaces_current==404:
        return {"synced": None, "status":{"error":"Device not configured for netflow"}}
    else:
        if record_config_current.status_code==200:
            record_config_optimal={'Cisco-IOS-XE-flow:record': {'name': 'RETIA_RECORD', 'collect': {'application': {'name': {}}, 'counter': {'bytes': {}, 'packets': {}}, 'interface': {'output': {}}, 'routing': {'destination': {'as': {}}, 'source': {'as': {}}}, 'timestamp': {'sys-uptime': {'first': [None], 'last': [None]}}}, 'description': 'USED FOR RETIA, DO NOT CHANGE', 'match': {'interface': {'input': {}}, 'ipv4': {'destination': {'address': [None]}, 'protocol': [None], 'source': {'address': [None]}, 'tos': [None]}, 'transport': {'destination-port': [None], 'source-port': [None]}}}}
            if json.loads(record_config_current.text)==record_config_optimal:
                record_config_current_status="OK"
            else:
                record_config_current_status="NEED TO SYNC"
        else:
            record_config_current_status=record_config_current.text
        
        if exporter_config_current.status_code==200:
            interface_type=""
            interface_number=""
            for char in req_to_check["device_interface_to_filebeat"]:
                if char.isalpha():
                    interface_type+=char
                elif char.isdigit():
                    interface_number+=char
            exporter_config_optimal={'Cisco-IOS-XE-flow:exporter': {'name': 'RETIA_EXPORTER', 'description': 'USED FOR RETIA, DO NOT CHANGE', 'destination': {'ipdest': {'ip': req_to_check["filebeat_host"]}}, 'option': {'application-attributes': {'timeout': 300}, 'application-table': {'timeout': 60}}, 'source': {str(interface_type): str(interface_number)}, 'template': {'data': {'timeout': 60}}, 'transport': {'udp': req_to_check["filebeat_port"]}}}
            if json.loads(exporter_config_current.text)==exporter_config_optimal:
                exporter_config_current_status="OK"
            else:
                exporter_config_current_status="NEED TO SYNC"
        else:
            exporter_config_current_status=record_config_current.text

        if monitor_config_current.status_code==200:
            monitor_config_optimal={'Cisco-IOS-XE-flow:monitor': {'name': 'RETIA_MONITOR', 'cache': {'timeout': {'active': 60}}, 'description': 'USED FOR RETIA, DO NOT CHANGE', 'exporter': [{'name': 'RETIA_EXPORTER'}], 'record': {'type': 'RETIA_RECORD'}}}
            if json.loads(monitor_config_current.text)==monitor_config_optimal:
                monitor_config_current_status="OK"
            else:
                monitor_config_current_status="NEED TO SYNC"
        else:
            monitor_config_current_status=record_config_current.text

        # Check applied flow in interface configuration
        interface_type=""
        interface_number=""
        for char in req_to_check["device_interface_to_server"]:
            if char.isalpha():
                interface_type+=char
            elif char.isdigit():
                interface_number+=char
        interfaces_current_data=json.loads(interfaces_current.text)['Cisco-IOS-XE-native:interface']
        flow_monitor_applied_to_correct_interface=True
        for interface_types in interfaces_current_data:
            for interface in interfaces_current_data[interface_types]:
                try:
                    flow_interface_setting=interface["ip"]["Cisco-IOS-XE-flow:flow"]["monitor"][0]
                    print(flow_interface_setting)
                    if flow_interface_setting=={'name': 'RETIA_MONITOR', 'output': [None]}:
                        if interface_types == interface_type and interface["name"] == interface_number:
                            flow_monitor_applied_to_correct_interface*=True
                        else:
                            flow_monitor_applied_to_correct_interface*=False
                    else:
                        flow_monitor_applied_to_correct_interface*=False
                except:
                    if interface_types == interface_type and interface["name"] == interface_number:
                        flow_monitor_applied_to_correct_interface*=False
                    else:
                        flow_monitor_applied_to_correct_interface*=True

        if flow_monitor_applied_to_correct_interface==True:
            flow_monitor_applied_to_correct_interface="OK"
        else:
            flow_monitor_applied_to_correct_interface="NEED TO SYNC"


        if record_config_current_status=="OK" and exporter_config_current_status=="OK" and monitor_config_current_status=="OK":
            synced=True
        else:
            synced=False
        return {"synced": synced, "status":{"flow_record":record_config_current_status, "flow_exporter":exporter_config_current_status, "flow_monitor":monitor_config_current_status, "applied_to_interface":flow_monitor_applied_to_correct_interface}}

def sync_device_detector_config(conn_strings:dict, req_to_change:dict)->dict:
    # Sync flow record, exporter, monitor
    interface_type=""
    interface_number=""
    for char in req_to_change["device_interface_to_filebeat"]:
        if char.isalpha():
            interface_type+=char
        elif char.isdigit():
            interface_number+=char
    body=json.dumps({"Cisco-IOS-XE-native:flow":{'Cisco-IOS-XE-flow:record': [{'name': 'RETIA_RECORD', 'collect': {'application': {'name': {}}, 'counter': {'bytes': {}, 'packets': {}}, 'interface': {'output': {}}, 'routing': {'destination': {'as': {}}, 'source': {'as': {}}}, 'timestamp': {'sys-uptime': {'first': [None], 'last': [None]}}}, 'description': 'USED FOR RETIA, DO NOT CHANGE', 'match': {'interface': {'input': {}}, 'ipv4': {'destination': {'address': [None]}, 'protocol': [None], 'source': {'address': [None]}, 'tos': [None]}, 'transport': {'destination-port': [None], 'source-port': [None]}}}], 'Cisco-IOS-XE-flow:exporter': [{'name': 'RETIA_EXPORTER', 'description': 'USED FOR RETIA, DO NOT CHANGE', 'destination': {'ipdest': {'ip': req_to_change["filebeat_host"]}}, 'option': {'application-attributes': {'timeout': 300}, 'application-table': {'timeout': 60}}, 'source': {str(interface_type): str(interface_number)}, 'template': {'data': {'timeout': 60}}, 'transport': {'udp': req_to_change["filebeat_port"]}}],'Cisco-IOS-XE-flow:monitor': [{'name': 'RETIA_MONITOR', 'cache': {'timeout': {'active': 60}}, 'description': 'USED FOR RETIA, DO NOT CHANGE', 'exporter': [{'name': 'RETIA_EXPORTER'}], 'record': {'type': 'RETIA_RECORD'}}]}}, indent=2)
    response_flow_config=putSomething(conn_strings, "/Cisco-IOS-XE-native:flow", body)
    del body


    # Sync apply flow to interface
    ## Delete all flow in all interface
    interfaces_current=getSomething(conn_strings, "/interface")
    interfaces_current_data=json.loads(interfaces_current.text)['Cisco-IOS-XE-native:interface']
    for interface_types in interfaces_current_data:
        for interface in interfaces_current_data[interface_types]:
            try:
                delSomething(conn_strings=conn_strings, path="/interface/%s=%s/ip/flow"%(interface_type, interface["name"]))
            except:
                pass

    ## Add flow to correct interface
    interface_type=""
    interface_number=""
    for char in req_to_change["device_interface_to_server"]:
        if char.isalpha():
            interface_type+=char
        elif char.isdigit():
            interface_number+=char
    body=json.dumps({ "Cisco-IOS-XE-flow:flow": { "monitor": [ { "name": "RETIA_MONITOR", "output": [None] } ] } })
    response_interface_flow_config=putSomething(conn_strings, "/interface/%s=%s/ip/flow"%(interface_type, interface_number), body)


    if response_flow_config.status_code==204 and response_interface_flow_config.status_code==204:
        return {"code":status.HTTP_204_NO_CONTENT}
    else:
        try:
            response_body_flow_config=json.loads(response_flow_config.text)
        except:
            response_body_flow_config={}

        try:
            response_body_interface_flow_config=json.loads(response_interface_flow_config.text)
        except:
            response_body_interface_flow_config={}

        return {"code":status.http_502_BAD_GATEWAY, "body":{"flow_config":response_body_flow_config, "flow_interface_config": response_body_interface_flow_config}}

def del_device_detector_config(conn_strings:dict)->dict:
    # Delete all flow in all interface
    interfaces_current=getSomething(conn_strings, "/interface")
    interfaces_current_data=json.loads(interfaces_current.text)['Cisco-IOS-XE-native:interface']
    for interface_types in interfaces_current_data:
        for interface in interfaces_current_data[interface_types]:
            try:
                delSomething(conn_strings=conn_strings, path="/interface/%s=%s/ip/flow"%(interface_types, interface["name"]))
            except:
                pass

    # Delete flow
    flow_del_response=delSomething(conn_strings=conn_strings, path="/flow")
    
    try:
        response_body=json.loads(flow_del_response.text)
    except:
        response_body={}
    return {"code": flow_del_response.status_code, "body": response_body}