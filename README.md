# Automated deployment of ACI Floating SVI to connect to Kubernetes Calico BGP clusters

## Description

Based on the latest version of the best practices for Cisco ACI integration with Calico (2022 version white paper), this script automates the configuration of an ACI network to connect to a Calico BGP cluster by using the new features of ACI, such as Floating SVI, Dynamic BGP, etc.


## Features

Compared to the best practices white paper there are the following differences:

* Optimize traffic based on a specific scenario where a set of gateways (Ingress/LoadBalancer, etc.) exist within the cluster to expose services: This means that the route is not necessarily optimized if the service is published using host IP route of Service IP , but the access route of the service which is published through the Ingress Controller or LoadBalancer will not be affected too much.

* Maximize ACI visibility of traffic while reducing k8s node routes fluctuations: When k8s nodes have external interconnected shortcuts instead of ACI fabric (e.g. on the same ESXi host, Hyperflex or UCS-B series), it still allows ACI to see k8s nodes mutual traffic. This is achieved by unchecking the AS Override/Disable AS check. Although the k8s nodes are therefore not visible to each other for BGP routes, they can be replaced with static routes pointing to Secondary IP.

* Because Calico BGP routes are not considered for propagation between clusters, all Calico clusters use a consistent AS number (e.g., the default 64512).

* Simplified security measures, including not limiting the number of BGP routes received by the ACI, not doing encrypted authenticated BGP sessions, but limiting the specific BGP prefixes received and sent by the ACI. This simplifies the configuration.


## Limitations

* Currently, only 2 anchor leaf switches are supported for automated deployment.

* The automated deployment of the Kubernetes Calico cluster side is not included here, that part will be included in our CMP system.

* Note that the control-plate-endpoint address of the Kubernetes cluster must be  in-band routable; automated deployments do not take into account the routing adjustments that have to be configured when the address falls out-of-band, where some services will not work in Calico L3 mode (e.g. Metrics-server service)


## Environment

* Python 3+

* ACI 5.0 or above

* Nexus 9k-EX or above as ACI anchor leaf

##  ACI Pre-Configuration

* Pre-configured or use existing L3/Physic Domain and AEP: Multiple k8s clusters can share one set of L3/Physic Domain and AEP settings, but VLAN-id shouldn't overlap with others. ESXis' Port Interface Policy Group already has AEPs associated with the above domains.

* Pre-configured or use existing VRF and BD: Each new k8s cluster occupies a single set of VRF and BD.

* Before running the script, give the following parameters in the input_data.py file.

  * Tenant, VRF where the Floating L3out is located
  * L3 Domain and Physic Domain name
  * An available VLAN-id in the VLAN Pool associated with the above Domains
  * The k8s cluster name and an id used for differentiation
  * k8s AS number
  * k8s addresses: Node Subnet, Service Subnet, Pod Subnet, External SVC Subnet (if any)


## Usage

### input_data.py

Initialization parameters are configured here.

### aci_calico_l3.py

Run this script directly to complete the automated configuration of the ACI.

### tp_....py

If you wish to modify the content of the original API resources, you can directly modify the JSON templates for these Managed Objects APIs here.
