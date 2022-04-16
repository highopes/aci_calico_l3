# k2 at MMS-tn
# Pre-configured
ACI_POD = '1'
ACI_LEAF1 = '101'  # MUST BE 1 - 254
ACI_LEAF2 = '102'  # MUST BE 1 - 254
TENANT = 'MMS-tn'
VRF = 'MMS-k2-VRF'
BD = ''
VLAN_ID = '802'
L3_DOMAIN = 'hangwe-floating-l3o-l3domain'
PHYSIC_DOMAIN = 'hangwe-floating-l3o-phdomain'

K8S_NAME = 'k'
K8S_ID = '2'  # MUST BE 0 - 254
K8S_AS = '64512'

# From CMP
NODE_SUBNET = "192.168.2.0/24"  # MUST BE x.x.x.0/yy  yy<=24
SERVICE_SUBNET = "10.152.0.0/16"
POD_SUBNET = "10.202.0.0/16"
EX_SERVICE_SUBNET = "192.168.152.0/24"
