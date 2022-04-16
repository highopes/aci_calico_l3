#!/usr/bin/env python
###################################################################################
#                           Written by Wei, Hang                                  #
#                          weihang_hank@gmail.com                                 #
###################################################################################
"""
Automatically config ACI Floating SVI to connect Calico BGP nodes.
Based on Cisco ACI/Calico Best Practice 2.0, but with some enhancements.
"""
import requests
import json
import time
from credentials import *
from my_py.aci_calico_l3.input_data import *
from my_py.aci_calico_l3.tp_l3extOut import *
from my_py.aci_calico_l3.tp_rtctrlSubjP import *
from my_py.aci_calico_l3.tp_bgpBestPathCtrlPol import *
from my_py.aci_calico_l3.tp_bgpCtxAfP import *
from my_py.aci_calico_l3.tp_CtxToBgpCtxAfP import *
from my_py.aci_calico_l3.tp_bgpCtxPol import *

requests.packages.urllib3.disable_warnings()

# Global parameter (Shared with other cluster, change with caution)
BGP_PATH = "mms-floating-l3o-path"
BGP_TIMER = "mms-floating-l3o-timer"
BGP_ECMP = "mms-floating-l3o-ecmp"

# Global parameter (Dedicated to the cluster to be deployed)
L3OUT = TENANT + '-' + K8S_NAME + K8S_ID + '-floating-svi'
EXT_EPG = TENANT + '-' + K8S_NAME + K8S_ID + 'extEPG'
NODE_PROFILE = L3OUT + '_nodeProfile'
INTERFACE_PROFILE = L3OUT + '_interfaceProfile'
NODE1_PATH = 'topology/pod-' + ACI_POD + '/node-' + ACI_LEAF1
NODE2_PATH = 'topology/pod-' + ACI_POD + '/node-' + ACI_LEAF2
ROUTER_ID1 = '192.' + K8S_ID + '.' + ACI_LEAF1 + '.' + ACI_LEAF1
ROUTER_ID2 = '192.' + K8S_ID + '.' + ACI_LEAF2 + '.' + ACI_LEAF2
PRIMARY_IP1 = NODE_SUBNET.replace('.0/', '.' + ACI_LEAF1 + '/')
PRIMARY_IP2 = NODE_SUBNET.replace('.0/', '.' + ACI_LEAF2 + '/')
SECONDARY_IP = NODE_SUBNET.replace('.0/', '.2/')
FLOATING_IP = NODE_SUBNET.replace('.0/', '.250/')
ROUTE_CONTROL = TENANT + '-' + K8S_NAME + K8S_ID + '-RouteControl'
CHANGE_FLAG = 'Nothing Changed'

# Login ACI
url = URL
payload = '''
{{ 
    "aaaUser": {{ 
        "attributes": {{ 
            "name": "{}", 
            "pwd": "{}" 
        }} 
    }} 
}}
'''
headers = {
    'Content-Type': 'text/plain'
}

response = requests.request("POST", url + "/api/aaaLogin.json", headers=headers,
                            data=payload.format(LOGIN, PASSWORD)).json()
token = response["imdata"][0]["aaaLogin"]["attributes"]["token"]

headers = {
    'Content-Type': 'application/json',
    'Cookie': 'APIC-cookie=' + token
}


def push_config(parent_dn, body):
    """
    push config
    """
    global CHANGE_FLAG

    print('Pushing config {} at {}'.format(body, parent_dn))
    try:
        response = requests.request("POST", url + '/api/node/mo/' + parent_dn + '.json', headers=headers, data=body)
        response.raise_for_status()
    except requests.HTTPError as e:
        print(e)
        print("status_code", response.status_code)
        exit(1)

    # response = requests.request("GET", url + '/api/node/class/fvTenant.json', headers=headers, data={})

    CHANGE_FLAG = 'Config Changed'
    print('    ... successfully')


def check_config(dn):
    """
    check config, return the item number
    """
    try:
        response = requests.request("GET", url + '/api/node/mo/' + dn + '.json', headers=headers,
                                    data='')
        response.raise_for_status()
    except requests.HTTPError as e:
        print(e)
        print("status_code", response.status_code)

    return int(response.json()['totalCount'])


def main():
    """
    This is main function ...
    """

    DESCR = 'Auto-configured by MMS at ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # *** BGP Best Path Control Policy: Relax AS-Path restriction when choosing multipaths ***
    if not check_config('uni/tn-' + TENANT + '/bestpath-' + BGP_PATH):
        bgpBestPath["imdata"][0]["bgpBestPathCtrlPol"]["attributes"]["name"] = BGP_PATH
        bgpBestPath["imdata"][0]["bgpBestPathCtrlPol"]["attributes"]["descr"] = DESCR
        push_config("uni/tn-" + TENANT, json.dumps(bgpBestPath))
    else:
        print("BGP Best Path Control Policy Object ({}) already exists!".format(BGP_PATH))

    # *** BGP Context Address Family Policy: Maximize ECMP number ***
    if not check_config('uni/tn-' + TENANT + '/bgpCtxAfP-' + BGP_ECMP):
        bgpCtxAfP["imdata"][0]["bgpCtxAfPol"]["attributes"]["name"] = BGP_ECMP
        bgpCtxAfP["imdata"][0]["bgpCtxAfPol"]["attributes"]["descr"] = DESCR
        push_config("uni/tn-" + TENANT, json.dumps(bgpCtxAfP))
    # Associate to VRF
    ctxToBgp_DN = 'uni/tn-' + TENANT + '/ctx-' + VRF + '/rsctxToBgpCtxAfPol-[' + BGP_ECMP + ']-ipv4-ucast'
    if not check_config(ctxToBgp_DN):
        CtxToBgpCtxAfPol["imdata"][0]["fvRsCtxToBgpCtxAfPol"]["attributes"]["dn"] = ctxToBgp_DN
        CtxToBgpCtxAfPol["imdata"][0]["fvRsCtxToBgpCtxAfPol"]["attributes"]["tnBgpCtxAfPolName"] = BGP_ECMP
        push_config('uni/tn-' + TENANT + '/ctx-' + VRF, json.dumps(CtxToBgpCtxAfPol))
    else:
        print("BGP AF Policy on ECMP ({}) already exists!".format(BGP_ECMP))

    # *** BGP Context Policy: BGP Timer Setting to match Calico's default timer ***
    if not check_config('uni/tn-' + TENANT + '/bgpCtxP-' + BGP_TIMER):
        bgpCtxPol["imdata"][0]["bgpCtxPol"]["attributes"]["name"] = BGP_TIMER
        bgpCtxPol["imdata"][0]["bgpCtxPol"]["attributes"]["descr"] = DESCR
        push_config("uni/tn-" + TENANT, json.dumps(bgpCtxPol))
    else:
        print("BGP Context Policy on Timer ({}) already exists!".format(BGP_TIMER))

    # *** Route Control Match Rules ***  Note that the name is not the same as the current PM Lab network
    if not check_config('uni/tn-' + TENANT + '/subj-' + ROUTE_CONTROL):
        rtctrlSubjP["imdata"][0]["rtctrlSubjP"]["attributes"]["descr"] = DESCR
        rtctrlSubjP["imdata"][0]["rtctrlSubjP"]["attributes"]["name"] = ROUTE_CONTROL

        rtctrlSubjP["imdata"][0]["rtctrlSubjP"]["children"][0]["rtctrlMatchRtDest"]["attributes"]["ip"] = NODE_SUBNET
        rtctrlSubjP["imdata"][0]["rtctrlSubjP"]["children"][1]["rtctrlMatchRtDest"]["attributes"]["ip"] = POD_SUBNET
        rtctrlSubjP["imdata"][0]["rtctrlSubjP"]["children"][2]["rtctrlMatchRtDest"]["attributes"][
            "ip"] = EX_SERVICE_SUBNET
        rtctrlSubjP["imdata"][0]["rtctrlSubjP"]["children"][3]["rtctrlMatchRtDest"]["attributes"]["ip"] = SERVICE_SUBNET
        # if you want to add more subnets to be propagated by BGP, add them as following
        # rtctrlSubjP["imdata"][0]["rtctrlSubjP"]["children"][4]["rtctrlMatchRtDest"]["attributes"]["ip"] = "x.x.x.x/xx"

        push_config("uni/tn-" + TENANT, json.dumps(rtctrlSubjP))
    else:
        print("Route Control Match Rules Object ({}) already exists!".format(ROUTE_CONTROL))

    # *** Floating SVI ***
    if not check_config('uni/tn-' + TENANT + '/out-' + L3OUT):
        l3extOut["imdata"][0]["l3extOut"]["attributes"]["descr"] = DESCR
        l3extOut["imdata"][0]["l3extOut"]["attributes"]["name"] = L3OUT

        l3extOut["imdata"][0]["l3extOut"]["children"][1]["l3extInstP"]["attributes"]["name"] = EXT_EPG

        ###
        l3extOut["imdata"][0]["l3extOut"]["children"][1]["l3extInstP"]["children"][1]["l3extSubnet"]["attributes"][
            "ip"] = NODE_SUBNET
        l3extOut["imdata"][0]["l3extOut"]["children"][1]["l3extInstP"]["children"][2]["l3extSubnet"]["attributes"][
            "ip"] = SERVICE_SUBNET
        l3extOut["imdata"][0]["l3extOut"]["children"][1]["l3extInstP"]["children"][3]["l3extSubnet"]["attributes"][
            "ip"] = POD_SUBNET

        ###
        l3extOut["imdata"][0]["l3extOut"]["children"][2]["l3extLNodeP"]["attributes"]["name"] = NODE_PROFILE
        l3extOut["imdata"][0]["l3extOut"]["children"][2]["l3extLNodeP"]["children"][0]["bgpProtP"]["children"][0][
            "bgpRsBestPathCtrlPol"]["attributes"]["tnBgpBestPathCtrlPolName"] = BGP_PATH
        l3extOut["imdata"][0]["l3extOut"]["children"][2]["l3extLNodeP"]["children"][0]["bgpProtP"]["children"][1][
            "bgpRsBgpNodeCtxPol"]["attributes"]["tnBgpCtxPolName"] = BGP_TIMER

        ###
        l3extOut["imdata"][0]["l3extOut"]["children"][2]["l3extLNodeP"]["children"][1]["l3extRsNodeL3OutAtt"][
            "attributes"][
            "rtrId"] = ROUTER_ID2
        l3extOut["imdata"][0]["l3extOut"]["children"][2]["l3extLNodeP"]["children"][1]["l3extRsNodeL3OutAtt"][
            "attributes"][
            "tDn"] = NODE2_PATH

        ###
        l3extOut["imdata"][0]["l3extOut"]["children"][2]["l3extLNodeP"]["children"][2]["l3extRsNodeL3OutAtt"][
            "attributes"][
            "rtrId"] = ROUTER_ID1
        l3extOut["imdata"][0]["l3extOut"]["children"][2]["l3extLNodeP"]["children"][2]["l3extRsNodeL3OutAtt"][
            "attributes"][
            "tDn"] = NODE1_PATH

        ###
        l3extOut["imdata"][0]["l3extOut"]["children"][2]["l3extLNodeP"]["children"][3]["l3extLIfP"]["attributes"][
            "name"] = INTERFACE_PROFILE

        ###
        l3extOut["imdata"][0]["l3extOut"]["children"][2]["l3extLNodeP"]["children"][3]["l3extLIfP"]["children"][5][
            "l3extVirtualLIfP"]["attributes"]["addr"] = PRIMARY_IP2
        l3extOut["imdata"][0]["l3extOut"]["children"][2]["l3extLNodeP"]["children"][3]["l3extLIfP"]["children"][5][
            "l3extVirtualLIfP"]["attributes"]["encap"] = 'vlan-' + VLAN_ID
        l3extOut["imdata"][0]["l3extOut"]["children"][2]["l3extLNodeP"]["children"][3]["l3extLIfP"]["children"][5][
            "l3extVirtualLIfP"]["attributes"]["nodeDn"] = NODE2_PATH
        l3extOut["imdata"][0]["l3extOut"]["children"][2]["l3extLNodeP"]["children"][3]["l3extLIfP"]["children"][5][
            "l3extVirtualLIfP"]["children"][0]["bgpPeerP"]["attributes"]["addr"] = NODE_SUBNET
        l3extOut["imdata"][0]["l3extOut"]["children"][2]["l3extLNodeP"]["children"][3]["l3extLIfP"]["children"][5][
            "l3extVirtualLIfP"]["children"][0]["bgpPeerP"]["children"][0]["bgpAsP"]["attributes"]["asn"] = K8S_AS
        l3extOut["imdata"][0]["l3extOut"]["children"][2]["l3extLNodeP"]["children"][3]["l3extLIfP"]["children"][5][
            "l3extVirtualLIfP"]["children"][1]["l3extIp"]["attributes"]["addr"] = SECONDARY_IP
        l3extOut["imdata"][0]["l3extOut"]["children"][2]["l3extLNodeP"]["children"][3]["l3extLIfP"]["children"][5][
            "l3extVirtualLIfP"]["children"][2]["l3extRsDynPathAtt"]["attributes"]["floatingAddr"] = FLOATING_IP
        l3extOut["imdata"][0]["l3extOut"]["children"][2]["l3extLNodeP"]["children"][3]["l3extLIfP"]["children"][5][
            "l3extVirtualLIfP"]["children"][2]["l3extRsDynPathAtt"]["attributes"]["tDn"] = 'uni/phys-' + PHYSIC_DOMAIN

        ###
        l3extOut["imdata"][0]["l3extOut"]["children"][2]["l3extLNodeP"]["children"][3]["l3extLIfP"]["children"][6][
            "l3extVirtualLIfP"]["attributes"]["addr"] = PRIMARY_IP1
        l3extOut["imdata"][0]["l3extOut"]["children"][2]["l3extLNodeP"]["children"][3]["l3extLIfP"]["children"][6][
            "l3extVirtualLIfP"]["attributes"]["encap"] = 'vlan-' + VLAN_ID
        l3extOut["imdata"][0]["l3extOut"]["children"][2]["l3extLNodeP"]["children"][3]["l3extLIfP"]["children"][6][
            "l3extVirtualLIfP"]["attributes"]["nodeDn"] = NODE1_PATH
        l3extOut["imdata"][0]["l3extOut"]["children"][2]["l3extLNodeP"]["children"][3]["l3extLIfP"]["children"][6][
            "l3extVirtualLIfP"]["children"][0]["bgpPeerP"]["attributes"]["addr"] = NODE_SUBNET
        l3extOut["imdata"][0]["l3extOut"]["children"][2]["l3extLNodeP"]["children"][3]["l3extLIfP"]["children"][6][
            "l3extVirtualLIfP"]["children"][0]["bgpPeerP"]["children"][0]["bgpAsP"]["attributes"]["asn"] = K8S_AS
        l3extOut["imdata"][0]["l3extOut"]["children"][2]["l3extLNodeP"]["children"][3]["l3extLIfP"]["children"][6][
            "l3extVirtualLIfP"]["children"][1]["l3extIp"]["attributes"]["addr"] = SECONDARY_IP
        l3extOut["imdata"][0]["l3extOut"]["children"][2]["l3extLNodeP"]["children"][3]["l3extLIfP"]["children"][6][
            "l3extVirtualLIfP"]["children"][2]["l3extRsDynPathAtt"]["attributes"]["floatingAddr"] = FLOATING_IP
        l3extOut["imdata"][0]["l3extOut"]["children"][2]["l3extLNodeP"]["children"][3]["l3extLIfP"]["children"][6][
            "l3extVirtualLIfP"]["children"][2]["l3extRsDynPathAtt"]["attributes"]["tDn"] = 'uni/phys-' + PHYSIC_DOMAIN

        l3extOut["imdata"][0]["l3extOut"]["children"][3]["l3extRsEctx"]["attributes"]["tnFvCtxName"] = VRF

        l3extOut["imdata"][0]["l3extOut"]["children"][4]["l3extRsL3DomAtt"]["attributes"][
            "tDn"] = 'uni/l3dom-' + L3_DOMAIN

        l3extOut["imdata"][0]["l3extOut"]["children"][5]["rtctrlProfile"]["children"][0]["rtctrlCtxP"]["children"][0][
            "rtctrlRsCtxPToSubjP"]["attributes"][
            "tnRtctrlSubjPName"] = TENANT + '-' + K8S_NAME + K8S_ID + '-RouteControl'
        l3extOut["imdata"][0]["l3extOut"]["children"][6]["rtctrlProfile"]["children"][0]["rtctrlCtxP"]["children"][0][
            "rtctrlRsCtxPToSubjP"]["attributes"][
            "tnRtctrlSubjPName"] = TENANT + '-' + K8S_NAME + K8S_ID + '-RouteControl'

        push_config("uni/tn-" + TENANT, json.dumps(l3extOut))

    else:
        print("Floating SVI L3out Object ({}) already exists!".format(L3OUT))

    print(CHANGE_FLAG)


if __name__ == '__main__':
    main()
