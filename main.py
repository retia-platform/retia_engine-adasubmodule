from operations import interface


global_ipaddr="192.168.137.1"
global_port="443"
global_auth=("retia", "retia00!")
global_header={"Content-Type": "application/yang-data+json", "Accept": "application/yang-data+json"}

# print(getInterface(global_ipaddr, global_port, global_auth, global_header))
# print(getInterfaceList(global_ipaddr, global_port, global_auth, global_header))
print(interface.getList(global_ipaddr, global_port, global_auth, global_header))