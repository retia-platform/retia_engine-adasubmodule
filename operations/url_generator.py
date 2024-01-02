def urlGenerator(ipaddr: str, port: str, module: str, container: str, leaf: str = "", leaf_value: str = "", optional_params: str = ""):
    if len(leaf) > 1 :
        url="https://%s:%s/restconf/data/%s:%s/%s"%(ipaddr, port, module, container, leaf)
        if len(leaf_value) > 1:
            url=url+"="+leaf_value
    else:
        url= "https://%s:%s/restconf/data/%s:%s"%(ipaddr, port, module, container)
    if len(optional_params)>1:
        url=url+"?"+optional_params
    return url