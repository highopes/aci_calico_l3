l3extOut = {
    "imdata": [
        {
            "l3extOut": {
                "attributes": {
                    "descr": "",
                    "enforceRtctrl": "export,import",
                    "name": ""
                },
                "children": [
                    {
                        "bgpExtP": {
                            "attributes": {
                                "annotation": "",
                                "descr": "",
                                "nameAlias": "",
                                "userdom": ":all:common:"
                            }
                        }
                    },
                    {
                        "l3extInstP": {
                            "attributes": {
                                "name": ""
                            },
                            "children": [
                                {
                                    "fvRsCustQosPol": {
                                        "attributes": {
                                            "annotation": "",
                                            "tnQosCustomPolName": "",
                                            "userdom": "all"
                                        }
                                    }
                                },
                                {
                                    "l3extSubnet": {
                                        "attributes": {
                                            "ip": "",
                                            "name": "node_subnet"
                                        }
                                    }
                                },
                                {
                                    "l3extSubnet": {
                                        "attributes": {
                                            "ip": "",
                                            "name": "service_subnet"
                                        }
                                    }
                                },
                                {
                                    "l3extSubnet": {
                                        "attributes": {
                                            "ip": "",
                                            "name": "pod_subnet"
                                        }
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "l3extLNodeP": {
                            "attributes": {
                                "name": ""
                            },
                            "children": [
                                {
                                    "bgpProtP": {
                                        "attributes": {
                                            "annotation": "",
                                            "name": "",
                                            "nameAlias": "",
                                            "userdom": ":all:common:"
                                        },
                                        "children": [
                                            {
                                                "bgpRsBestPathCtrlPol": {
                                                    "attributes": {
                                                        "tnBgpBestPathCtrlPolName": ""
                                                    }
                                                }
                                            },
                                            {
                                                "bgpRsBgpNodeCtxPol": {
                                                    "attributes": {
                                                        "tnBgpCtxPolName": ""
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    "l3extRsNodeL3OutAtt": {
                                        "attributes": {
                                            "rtrId": "",
                                            "tDn": ""
                                        }
                                    }
                                },
                                {
                                    "l3extRsNodeL3OutAtt": {
                                        "attributes": {
                                            "rtrId": "",
                                            "tDn": ""
                                        }
                                    }
                                },
                                {
                                    "l3extLIfP": {
                                        "attributes": {
                                            "name": ""
                                        },
                                        "children": [
                                            {
                                                "l3extRsArpIfPol": {
                                                    "attributes": {
                                                        "tnArpIfPolName": ""
                                                    }
                                                }
                                            },
                                            {
                                                "l3extRsEgressQosDppPol": {
                                                    "attributes": {
                                                        "tnQosDppPolName": ""
                                                    }
                                                }
                                            },
                                            {
                                                "l3extRsIngressQosDppPol": {
                                                    "attributes": {
                                                        "tnQosDppPolName": ""
                                                    }
                                                }
                                            },
                                            {
                                                "l3extRsLIfPCustQosPol": {
                                                    "attributes": {
                                                        "tnQosCustomPolName": ""
                                                    }
                                                }
                                            },
                                            {
                                                "l3extRsNdIfPol": {
                                                    "attributes": {
                                                        "tnNdIfPolName": ""
                                                    }
                                                }
                                            },
                                            {
                                                "l3extVirtualLIfP": {
                                                    "attributes": {
                                                        "addr": "",
                                                        "encap": "",
                                                        "encapScope": "local",
                                                        "ifInstT": "ext-svi",
                                                        "mode": "regular",
                                                        "mtu": "9000",
                                                        "name": "",
                                                        "nodeDn": ""
                                                    },
                                                    "children": [
                                                        {
                                                            "bgpPeerP": {
                                                                "attributes": {
                                                                    "addr": "",
                                                                    "addrTCtrl": "af-ucast",
                                                                    "adminSt": "enabled"
                                                                },
                                                                "children": [
                                                                    {
                                                                        "bgpAsP": {
                                                                            "attributes": {
                                                                                "asn": ""
                                                                            }
                                                                        }
                                                                    },
                                                                    {
                                                                        "bgpRsPeerPfxPol": {
                                                                            "attributes": {
                                                                                "tnBgpPeerPfxPolName": ""
                                                                            }
                                                                        }
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            "l3extIp": {
                                                                "attributes": {
                                                                    "addr": "",
                                                                    "name": ""
                                                                }
                                                            }
                                                        },
                                                        {
                                                            "l3extRsDynPathAtt": {
                                                                "attributes": {
                                                                    "encap": "unknown",
                                                                    "floatingAddr": "",
                                                                    "tDn": ""
                                                                }
                                                            }
                                                        }
                                                    ]
                                                }
                                            },
                                            {
                                                "l3extVirtualLIfP": {
                                                    "attributes": {
                                                        "addr": "",
                                                        "encap": "",
                                                        "encapScope": "local",
                                                        "ifInstT": "ext-svi",
                                                        "mode": "regular",
                                                        "mtu": "9000",
                                                        "name": "",
                                                        "nodeDn": ""
                                                    },
                                                    "children": [
                                                        {
                                                            "bgpPeerP": {
                                                                "attributes": {
                                                                    "addr": "",
                                                                    "addrTCtrl": "af-ucast",
                                                                    "adminSt": "enabled"
                                                                },
                                                                "children": [
                                                                    {
                                                                        "bgpAsP": {
                                                                            "attributes": {
                                                                                "asn": ""
                                                                            }
                                                                        }
                                                                    },
                                                                    {
                                                                        "bgpRsPeerPfxPol": {
                                                                            "attributes": {
                                                                                "tnBgpPeerPfxPolName": ""
                                                                            }
                                                                        }
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            "l3extIp": {
                                                                "attributes": {
                                                                    "addr": "",
                                                                    "name": ""
                                                                }
                                                            }
                                                        },
                                                        {
                                                            "l3extRsDynPathAtt": {
                                                                "attributes": {
                                                                    "encap": "unknown",
                                                                    "floatingAddr": "",
                                                                    "tDn": ""
                                                                }
                                                            }
                                                        }
                                                    ]
                                                }
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "l3extRsEctx": {
                            "attributes": {
                                "tnFvCtxName": ""
                            }
                        }
                    },
                    {
                        "l3extRsL3DomAtt": {
                            "attributes": {
                                "tDn": ""
                            }
                        }
                    },
                    {
                        "rtctrlProfile": {
                            "attributes": {
                                "name": "default-import"
                            },
                            "children": [
                                {
                                    "rtctrlCtxP": {
                                        "attributes": {
                                            "action": "permit",
                                            "name": "import_subnets",
                                            "order": "0"
                                        },
                                        "children": [
                                            {
                                                "rtctrlRsCtxPToSubjP": {
                                                    "attributes": {
                                                        "tnRtctrlSubjPName": ""
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "rtctrlProfile": {
                            "attributes": {
                                "name": "default-export"
                            },
                            "children": [
                                {
                                    "rtctrlCtxP": {
                                        "attributes": {
                                            "action": "permit",
                                            "name": "export_subnets",
                                            "order": "0"
                                        },
                                        "children": [
                                            {
                                                "rtctrlRsCtxPToSubjP": {
                                                    "attributes": {
                                                        "annotation": "",
                                                        "tnRtctrlSubjPName": ""
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }
    ]
}
