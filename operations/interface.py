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
    
def set(ipaddr: str, port: str,  credential: tuple, header: dict, interface_name: str, req_to_change: dict):
    target_url=urlGenerator(ipaddr, port, "ietf-interfaces", "interfaces", "interface", interface_name)
    update_body=get(ipaddr, port, credential, header, interface_name)["body"]
    # Interface Description
    if len(req_to_change["description"])>0:
        update_body["description"]=req_to_change["description"]
    else:
        if "description" in update_body:
            del update_body["description"]

    # Interface Addr
    if len(req_to_change["ip"])>0 and len(req_to_change["netmask"])>0:
        if "address" in update_body:
            del update_body["ietf-ip:ipv4"]["address"]    
        update_body["ietf-ip:ipv4"]={"address":[{}]}
        update_body["ietf-ip:ipv4"]["address"][0]["ip"]=req_to_change["ip"]
        update_body["ietf-ip:ipv4"]["address"][0]["netmask"]=req_to_change["netmask"]
    else:
        del update_body["ietf-ip:ipv4"]["address"]

    # Interface enable
    update_body["enabled"]=req_to_change["enabled"]

    update_body=json.dumps({"ietf-interfaces:interface":update_body})
    response=requests.put(url=target_url, auth=credential, headers=header, data=update_body, verify=False)
    return {"code": response.status_code, "body":response.text}

    





    # target_url=urlGenerator(ipaddr, port, "ietf-interfaces", "interfaces", "interface", interface_name)
    # update_body=json.dumps({"ietf-interfaces:interface":update_body})
    # print(update_body)
    # response = requests.put(url=target_url, auth=credential, headers=header, data=update_body, verify=False)

    # try:
    #     if len(interface_name) > 1:
    #         response_body=json.loads(response.text)
    #         response_body=response_body["ietf-interfaces:interface"]
    #     else:
    #         response_body=json.loads(response.text)
    #         response_body=response_body["ietf-interfaces:interfaces"]["interface"]
    # except:
    #     response_body = {}

    # return {"code" : response.status_code, "body" : response_body}

