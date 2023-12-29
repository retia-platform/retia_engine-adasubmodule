import requests, json

global_ipaddr="192.168.137.1"
global_port="443"
global_auth=("retia", "retia00!")
global_header={"Content-Type": "application/yang-data+json", "Accept": "application/yang-data+json"}


def urlGenerator(ipaddr: str, port: str, module: str, container: str, leaf: str = "", leaf_value: str = ""):
    if len(leaf) > 1 and len(leaf_value)>1:
        return "https://%s:%s/restconf/data/%s:%s/%s=%s"%(ipaddr, port, module, container, leaf, leaf_value)
    else:
        return "https://%s:%s/restconf/data/%s:%s"%(ipaddr, port, module, container)



def getInterface(ipaddr: str, port: str,  credential: tuple, header: dict, interface_name: str = ""):
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
    
def setInterface(ipaddr: str, port: str,  credential: tuple, header: dict, interface_name: str, req_to_change: dict):
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
    print(update_body)
    # response = requests.patch(url=target_url, auth=credential, headers=header, data=update_body, verify=False)
    # print(response)



# print(getInterface(global_ipaddr, global_port, global_auth, global_header, "GigabitEthernet1"))

setInterface(global_ipaddr, global_port, global_auth, global_header, "GigabitEthernet2", {"description":"asdasd","ip":"123.123.13.1", "netmask":"255.255.255.0"})