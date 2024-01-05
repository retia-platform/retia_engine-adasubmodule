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

# print(createOspfProcess({"ipaddr": global_ipaddr, "port": global_port, "credential": global_auth}, {"id":10}))
# print(setOspfProcessDetail({"ipaddr": global_ipaddr, "port": global_port, "credential": global_auth}, {"id":10, "default-information-originate":"true", "network":[{"ip":"10.0.0.4","wildcard":"0.0.0.3","area":0},{"ip":"10.0.0.8","wildcard":"0.0.0.3","area":0}],"passive-interface":["GigabitEthernet1","GigabitEthernet4","GigabitEthernet5"],"redistribute":["connected"]}))
# print(delOspfProcess({"ipaddr": global_ipaddr, "port": global_port, "credential": global_auth}, {"id":10}))
# print(getOspfProcessDetail({"ipaddr": global_ipaddr, "port": global_port, "credential": global_auth},{"id":10}))

print(setInterfaceDetail({"ipaddr": global_ipaddr, "port": global_port, "credential": global_auth}, {"name":"GigabitEthernet2", "enabled":True, "ip":"10.0.0.5", "netmask":"255.255.255.252"}))
