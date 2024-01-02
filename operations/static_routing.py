from operations.url_generator import urlGenerator
import requests, json

def get(ipaddr: str, port: str,  credential: tuple, header: dict):
    target_url = "https://%s:%s/restconf/data/ietf-routing:routing/routing-instance=default/routing-protocols/routing-protocol"%(ipaddr,port)
    response = requests.get(url=target_url, auth=credential, headers=header, verify=False)
    response_code=response.status_code
    response_body=json.loads(response.text)
    response_body=response_body["ietf-routing:routing-protocol"][0]["static-routes"]
    return {"code" : response_code, "body" : response_body}

def set(ipaddr: str, port: str,  credential: tuple, header: dict, req_to_change: list):
    target_url = "https://%s:%s/restconf/data/ietf-routing:routing/routing-instance=default/routing-protocols"%(ipaddr,port)
    update_body=json.loads(requests.get(url=target_url, auth=credential, headers=header, verify=False).text)

    # if len(req_to_change["destination-prefix"]) and len(req_to_change["next-hop-address"]):
    del update_body["ietf-routing:routing-protocols"]["routing-protocol"][0]["static-routes"]
    
    route_entry=[]
    for req_route in req_to_change:
        route_entry_dict={"destination-prefix":req_route["destination-prefix"],"next-hop":{"next-hop-address":req_route["next-hop-address"]}}
        route_entry.append(route_entry_dict)

    update_body["ietf-routing:routing-protocols"]["routing-protocol"][0]["static-routes"]={"ietf-ipv4-unicast-routing:ipv4":{"route":route_entry}}
    update_body=json.dumps(update_body, indent=2)
    response=requests.put(url=target_url, auth=credential, headers=header, data=update_body, verify=False)
    return {"code" : response.status_code, "body": response.text}