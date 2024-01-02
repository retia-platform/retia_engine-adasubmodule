def urlGenerator(ipaddr: str, port: str, module: str, container: str, leaf: str = "", leaf_value: str = ""):
    if len(leaf) > 1 and len(leaf_value)>1:
        return "https://%s:%s/restconf/data/%s:%s/%s=%s"%(ipaddr, port, module, container, leaf, leaf_value)
    else:
        return "https://%s:%s/restconf/data/%s:%s"%(ipaddr, port, module, container)