import requests, json
from operations.url_generator import urlGenerator

def getList(ipaddr: str, port: str,  credential: tuple, header: dict)->dict:
    target_url=urlGenerator(ipaddr, port, "ietf-interfaces", "interfaces", "interface")
    response=requests.get(url=target_url, auth=credential, headers=header, verify=False)
    response_code=response.status_code
    try:
        response_body=json.loads(response.text)
        response_body=response_body["ietf-interfaces:interfaces"]["interface"]
        response_body_interface_list=[]
        for interface_name in response_body:
            response_body_interface_list.append(interface_name["name"])
    except:
        response_body_interface_list = []

    return {"code" : response_code, "body" : response_body_interface_list}

    
def get(ipaddr: str, port: str,  credential: tuple, header: dict, interface_name: str = "")->dict:
    target_url=urlGenerator(ipaddr, port, "ietf-interfaces", "interfaces", "interface", interface_name)
    response=requests.get(url=target_url, auth=credential, headers=header, verify=False)
    response_code=response.status_code
    try:
        if len(interface_name) > 1:
            response_body=json.loads(response.text)
            response_body=response_body["ietf-interfaces:interface"]
        else:
            response_body=json.loads(response.text)
            response_body=response_body["ietf-interfaces:interfaces"]["interface"]
    except:
        response_body = {}

    return {"code" : response_code, "body" : response_body}
    
def set(ipaddr: str, port: str,  credential: tuple, header: dict, interface_name: str, req_to_change: dict)->dict:
    update_body={"ietf-ip:ipv4":{"address":[{}]}}
    if "description" in req_to_change:
        update_body.update({"description":req_to_change["description"]})
    if "enabled" in req_to_change:
        update_body.update({"enabled":req_to_change["enabled"]})
    if "ip" in req_to_change:
        # update_body.update({"ietf-ip:ipv4":{"address":[{"ip":req_to_change["ip"]}]}})
        update_body["ietf-ip:ipv4"]["address"][0]["ip"]=req_to_change["ip"]
    if "netmask" in req_to_change:
        update_body["ietf-ip:ipv4"]["address"][0]["netmask"]=req_to_change["netmask"]
    
    target_url=urlGenerator(ipaddr, port, "ietf-interfaces", "interfaces", "interface", interface_name)
    update_body={"ietf-interfaces:interface":update_body}
    update_body=json.dumps(update_body, indent=2)
    try:
        if len(interface_name) > 1:
            response_body=json.loads(response.text)
            response_body=response_body["ietf-interfaces:interface"]
        else:
            response_body=json.loads(response.text)
            response_body=response_body["ietf-interfaces:interfaces"]["interface"]
    except:
        response_body = {}

    response = requests.patch(url=target_url, auth=credential, headers=header, data=update_body, verify=False)
    return {"code" : response.status_code, "body" : response_body}

