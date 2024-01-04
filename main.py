from operation import *


global_ipaddr="192.168.137.1"
global_port="443"
global_auth=("retia", "retia00!")
global_header={"Content-Type": "application/yang-data+json", "Accept": "application/yang-data+json"}

# print(getInterface(global_ipaddr, global_port, global_auth, global_header))
# print(getInterfaceList(global_ipaddr, global_port, global_auth, global_header))
# print(interface.set(global_ipaddr,global_port, global_auth, global_header,"GigabitEthernet2",{"description":"ini desc","ip":"10.10.10.1", "netmask":"255.255.255.0", "enabled":"false"}))
# print(interface.get(global_ipaddr, global_port, global_auth, global_header))
# print(static_routing.set(global_ipaddr, global_port, global_auth, global_header, [{"destination-prefix":"0.0.0.0/0", "next-hop-address":"192.168.137.2"}]))

print(setPassEncryption({"ipaddr": global_ipaddr, "port": global_port, "credential": global_auth}, {"password-encryption":"true"}))
# print(getPassEncryption({"ipaddr": global_ipaddr, "port": global_port, "credential": global_auth}))
