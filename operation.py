import json, requests


def getSomething(conn_strings: dict, path: str):
    target_url="https://%s:%s/restconf/data/Cisco-IOS-XE-native:native%s"%(conn_strings["ipaddr"], conn_strings["port"], path)
    return requests.get(url=target_url, auth=conn_strings["credential"], headers={"Content-Type": "application/yang-data+json", "Accept": "application/yang-data+json"}, verify=False)

def patchSomething(conn_strings: dict, path: str, body: str):
    target_url="https://%s:%s/restconf/data/Cisco-IOS-XE-native:native%s"%(conn_strings["ipaddr"], conn_strings["port"], path)
    return requests.patch(url=target_url, auth=conn_strings["credential"], headers={"Content-Type": "application/yang-data+json", "Accept": "application/yang-data+json"}, data=body, verify=False)

def delSomething(conn_strings: dict, path: str):
    target_url="https://%s:%s/restconf/data/Cisco-IOS-XE-native:native%s"%(conn_strings["ipaddr"], conn_strings["port"], path)
    return requests.delete(url=target_url, auth=conn_strings["credential"], headers={"Content-Type": "application/yang-data+json", "Accept": "application/yang-data+json"}, verify=False)


def getVersion(conn_strings: dict)->dict:
    response=getSomething(conn_strings, "/version")
    return {"code": response.status_code, "body": json.loads(response.text)["Cisco-IOS-XE-native:version"]}

def getHostname(conn_strings: dict)->dict:
    response=getSomething(conn_strings, "/hostname")
    return {"code": response.status_code, "body": json.loads(response.text)["Cisco-IOS-XE-native:hostname"]}

def setHostname(conn_strings: dict, req_to_change: dict)->dict:
    body=json.dumps({"hostname": req_to_change["hostname"]})
    response=patchSomething(conn_strings, "/hostname", body)
    return {"code": response.status_code, "body": response.text}

def getLoginBanner(conn_strings)->dict:
    response=getSomething(conn_strings, "/banner/login")
    try:
        response_body=json.loads(response.text)["Cisco-IOS-XE-native:login"]["banner"]
    except:
        response_body={}
    return {"code": response.status_code, "body": response_body}

def setLoginBanner(conn_strings, req_to_change: dict):
    if len(req_to_change["banner_login"])>0:
        body=json.dumps({"login": {"banner": req_to_change["banner_login"]}},indent=2)
        response=patchSomething(conn_strings, "/banner/login", body)
    else:
        response=delSomething(conn_strings, "/banner/login")

    try:
        response_body=json.loads(response.text)
    except:
        response_body={}

    return {"code": response.status_code, "body": response_body}

def getMotdBanner(conn_strings)->dict:
    response=getSomething(conn_strings, "/banner/motd")
    try:
        response_body=json.loads(response.text)["Cisco-IOS-XE-native:motd"]["banner"]
    except:
        response_body={}
    return {"code": response.status_code, "body": response_body}

def setMotdBanner(conn_strings, req_to_change: dict):
    if len(req_to_change["banner_motd"])>0:
        body=json.dumps({"motd": {"banner": req_to_change["banner_motd"]}},indent=2)
        response=patchSomething(conn_strings, "/banner/motd", body)
    else:
        response=delSomething(conn_strings, "/banner/motd")
        
    try:
        response_body=json.loads(response.text)
    except:
        response_body={}
    return {"code": response.status_code, "body": response_body}

def getPassEncryption(conn_strings):
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
