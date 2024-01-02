from operations.url_generator import urlGenerator
import requests, json

def get(ipaddr: str, port: str,  credential: tuple, header: dict):
    target_url = "https://%s:%s/restconf/data/ietf-routing:routing/routing-instance=default/routing-protocols/routing-protocol"%(ipaddr,port)
    response = requests.get(url=target_url, auth=credential, headers=header, verify=False)
    response_code=response.status_code
    response_body=json.loads(response.text)
    response_body=response_body["ietf-routing:routing-protocol"][0]["static-routes"]
    print(response_body)